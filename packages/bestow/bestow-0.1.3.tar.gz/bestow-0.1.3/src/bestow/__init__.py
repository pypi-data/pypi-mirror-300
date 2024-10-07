# This file is part of Bestow.
# Copyright (C) 2024 Taylor Rodríguez.
#
# Bestow is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Bestow is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public
# License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with Bestow. If not, see
# <http://www.gnu.org/licenses/>.

"""Bestow: simple and secure file transfer CLI."""

__all__ = ["main", "__version__"]

import argparse
import asyncio
import errno
import importlib.metadata
import ipaddress
import socket
import sys

from bestow import log

try:
    __version__ = importlib.metadata.version(__package__)
except (ValueError, importlib.metadata.PackageNotFoundError):
    __version__ = "0.0.0"

# Define the range of dynamic/private ports. This helps to avoid
# conflicts with reserved ports or other registered ports.
MIN_PORT = 49152
MAX_PORT = 65535
# Define the default port to use for TCP connections.
BASE_PORT = 50222


def get_version() -> str:
    """Return the package version as a string."""
    return f"{__package__.capitalize()} version {__version__}"


def set_port(port_input: str, /) -> int:
    """Ensure that a port conforms with the dynamic port range."""
    try:
        port = int(port_input)
    except ValueError:
        raise argparse.ArgumentTypeError("port must be an integer")

    if port < MIN_PORT or port > MAX_PORT:
        raise argparse.ArgumentTypeError(
            f"port must be between {MIN_PORT} and {MAX_PORT}"
        )

    return port


def get_private_ipv4_address() -> str:
    """Determine the machine's private IP address."""
    log.trace("Attempting to determine private IP address")
    hostname = socket.gethostname()
    log.debug(f"Host name is {hostname!r}")

    # Determine the local IP addresses by resolving the host name.
    try:
        _, _, ip_addresses = socket.gethostbyname_ex(hostname)
    except socket.gaierror:
        log.error(f"Failed to resolve invalid hostname {hostname}")
    else:
        for address in ip_addresses:
            ip_address = ipaddress.ip_address(address)

            # Ignore public IP addresses.
            if not ip_address.is_private:
                log.trace(f"Skipped public address {ip_address}")
                continue

            # Ignore loopback addresses (eg. 127.0.0.1).
            if ip_address.is_loopback:
                log.trace(f"Skipped loopback address {ip_address}")
                continue

            log.trace("Got private IP address from resolved host name")
            return address

    # Determine the local IP address by from a UDP socket connection.
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.connect(("0.0.0.1", 53))
        address, _ = sock.getsockname()
        log.trace("Got private IP address from UDP socket name")
        return address


async def start_client(host: ipaddress._BaseAddress, port: int) -> None:
    """Send a message to the server and wait for a response."""
    log.debug("Running TCP client")
    log.debug(f"Host is {host}")
    log.trace("Attempting to create connection with host")

    try:
        reader, writer = await asyncio.open_connection(
            host=str(host), port=port
        )
    except OSError as e:
        log.debug(f"Errno {e.errno}: {errno.errorcode[e.errno]}")
        log.critical(e.strerror)
    else:
        log.trace("Established TCP connection with host")

    size = 100
    data = await reader.read(size)
    log.trace(f"Read {size} bytes of data from the stream")

    message = data.decode(encoding="utf-8")
    log.info(f"Received {message!r} from {host}:{port}")

    writer.write(data)
    await writer.drain()
    log.info(f"Echoed {message!r} back to {host}:{port}")

    writer.close()
    await writer.wait_closed()
    log.trace("Closed the stream writer object")


async def handle_client(
    reader: asyncio.StreamReader, writer: asyncio.StreamWriter, message: str
) -> None:
    """Receive a message from the client and echo it back."""
    host, port = writer.get_extra_info("peername")
    log.debug(f"New connection with {host}:{port}")

    writer.write(message.encode(encoding="UTF-8"))
    await writer.drain()
    log.info(f"Sent {message!r} to {host}:{port}")

    size = 100
    data = await reader.read(size)
    log.trace(f"Read {size} bytes of data from the stream")

    message = data.decode(encoding="utf-8")
    log.info(f"Received {message!r} from {host}:{port}")

    writer.close()
    await writer.wait_closed()
    log.trace("Closed the stream writer object")


    log.debug(f"Closed connection with {host}:{port}")


async def enumerate_server_ports(
    host: str, base_port: int, max_port: int, message: str
) -> asyncio.Server:
    """Enumerate port numbers until one is not in use."""
    log.trace(f"Enumerating server ports starting at {base_port}")

    for port in range(base_port, max_port + 1):
        try:
            server = await asyncio.start_server(
                lambda r, w: handle_client(r, w, message=message),
                host=host,
                port=port,
            )
        except OSError as e:
            # EADDRINUSE: Address already in use.
            if e.errno == errno.EADDRINUSE:
                log.warn(f"Port {port} is already in use, trying next port")
                log.trace(f"Incrementing port number to {port + 1}")
            else:
                # Exit if the errno is unexpected.
                log.debug(f"Errno {e.errno}: {errno.errorcode[e.errno]}")
                log.critical(e.strerror)
        else:
            return server

    log.critical("No available ports found")


async def start_server(port: int, message: str) -> None:
    log.debug("Running TCP server")

    try:
        host = get_private_ipv4_address()
    except OSError as e:
        log.debug(f"Errno {e.errno}: {errno.errorcode[e.errno]}")
        log.critical(e.strerror)

    log.debug(f"Address is {host}")

    server = await enumerate_server_ports(
        host=host, base_port=port, max_port=MAX_PORT, message=message
    )

    addr = "%s:%d"
    addresses = ", ".join(addr % sock.getsockname() for sock in server.sockets)
    log.info(f"Serving on {addresses}")

    async with server:
        log.trace("Starting to accept incoming connections")
        await server.serve_forever()


def handle_args() -> argparse.Namespace:
    """Parse command line arguments."""
    # Define the global parser. Any arguments added will be available
    # for any/all subcommands as well. This helps to reduce repetition.
    global_parser = argparse.ArgumentParser(add_help=False)
    global_parser.add_argument(
        "-v", "--version", action="version", version=get_version()
    )
    global_parser.add_argument(
        "--log-level",
        dest="log_level",
        default=log.DEFAULT,
        choices=log.LOG_LEVELS,
        help=f"set the logging level (default: {log.DEFAULT})",
    )
    global_parser.add_argument(
        "--no-colour",
        "--no-color",  # For any Americans...
        dest="show_colour",
        action="store_false",
        help="disable coloured output",
    )
    global_parser.add_argument(
        "-p",
        "--port",
        dest="port",
        type=set_port,
        default=BASE_PORT,
        help=f"port number to use for the connection (default: {BASE_PORT})",
    )

    # This parser is used to parse arguments and handles any subparsers.
    parser = argparse.ArgumentParser(
        parents=[global_parser],
        description="Simple and secure file transfer CLI",
        epilog=get_version(),
    )

    # Handle commands.
    commands = parser.add_subparsers(
        dest="command",
        required=True,
        description="Run `%(prog)s <command> --help` for more information",
    )

    # Parse arguments for the `start` command.
    description = "Provide files to the client"
    server_parser = commands.add_parser(
        parents=[global_parser],
        name="start",
        description=description,
        help=description.lower(),
    )
    server_parser.add_argument(
        "message", help="the message to send to the client"
    )

    # Parse arguments for the `connect` command.
    description = "Request files from the server"
    client_parser = commands.add_parser(
        parents=[global_parser],
        name="connect",
        description=description,
        help=description.lower(),
    )
    client_parser.add_argument(
        "host", type=ipaddress.ip_address, help="the IP address of the server"
    )

    # Default to `--help` if no arguments are provided to `bestow`.
    if (nargs := len(sys.argv)) == 1:
        default_args = ["--help"]
    # Default to `--help` if no arguments are provided to a subcommand.
    elif nargs == 2 and (command := sys.argv[1]) in commands._name_parser_map:
        default_args = [command, "--help"]
    else:
        default_args = None

    return parser.parse_args(args=default_args)


def main() -> None:
    """Run main the script."""
    args = handle_args()
    log.configure(level=args.log_level, colour=args.show_colour)
    log.debug(get_version())

    if args.command == "start":
        coroutine = start_server(port=args.port, message=args.message)
    elif args.command == "connect":
        coroutine = start_client(host=args.host, port=args.port)

    try:
        asyncio.run(coroutine)
    except KeyboardInterrupt:
        log.error("Keyboard interrupt")

    sys.exit(0)
