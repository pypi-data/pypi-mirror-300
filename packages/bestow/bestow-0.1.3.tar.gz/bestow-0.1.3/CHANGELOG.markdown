# Changelog

All notable changes to this project will be documented in this file.

<!--
## [Unreleased]

### Added

### Fixed

### Changed

### Removed
-->

## [0.1.3] - 2024-10-07

### Added

- Created a better output system, which cleanly displays error messages
  to the user without traceback.
  - New `--no-colour` flag to suppress coloured output for accessibility
    reasons. If output is redirected to a file, colour codes will
    automatically be stripped even without the flag.
  - New `--log-level` flag to control the level of logging shown to the
    user. The default is `info`, which shows relevant user-friendly
    information.
- Added `-v` flag, which is shorthand for `--version`.
- Properly handle more errors, which improves program robustness.
- When using `bestow connect <host>`, there are now checks to ensure a
  valid IPv4 or IPv6 address was provided.
- Added a required `message` positional argument for `bestow start`.
  Instead of the default "hello" message being sent, this new argument
  will be shared instead.

### Changed

- Swapped behaviour of core subcommands:
  - `bestow start`: Send a message to the client.
  - `bestow connect`: Receive a message from the server.
  - This better aligns with the final vision of the project, which is
    for the server to send file data to the client.
- Providing no arguments to a subcommand now shows the help message for
  that command.
  - `bestow connect` is equivalent to `bestow connect --help`.
  - `bestow start` is equivalent to `bestow start --help`.
  - This output is more intuitive and user friendly than an error
    message about missing arguments.
- Some flags are now parsed globally.
  - Before this change, certain flags could only be used exclusively
    before or exclusively after a subcommand.
  - Now, they can be used before or after any subcommand.
  - Global flags added:
    - `--version`/`-v`
    - `--port`/`-p`
    - `--no-colour`/`--no-color`
    - `--log-level`
  - `bestow --port 50000 connect <host>` is equivalent to
    `bestow connect --port 50000 <host>`.

### Fixed

- Fixed bugs when resolving the local IP address when using `bestow start`:
  - In rare cases, a loopback IP address was resolved instead of the
    local IP address.
  - On certain networks, a public IP address was sometimes resolved,
     causing an `EADDRNOTAVAIL` error.

## [0.1.2] - 2024-10-03

### Added

- Created the changelog to track changes in the project.
- Handle certain client errors better and display an error message.
- New `--version` flag to display the current version.
- New `--port` flag for controlling which port number to use.

### Changed

- The server now uses the machine's private IP address instead of
`127.0.0.1`, which allows clients on the local network to connect.
- Reworked the CLI interface to parse subcommands:
  - `bestow start` replaces `--server`.
  - `bestow connect` replaces `--client`.

## [0.1.1] - 2024-10-02

### Added

- Created package metadata and published package to [PyPI].
- Implemented a simple async client/server interface:
  - `bestow --server` runs the server, which listens for a message.
  - `bestow --client` runs the client, which sends a message.

## [0.1.0] - 2024-10-02

### Added

- Basic project layout.
- The foundation upon which **Bestow** will be built!

[PyPI]: https://pypi.org/project/bestow/
[unreleased]: https://codeberg.org/ViteByte/bestow/compare/v0.1.3...HEAD
[0.1.3]: https://codeberg.org/ViteByte/bestow/compare/v0.1.2...v0.1.3
[0.1.2]: https://codeberg.org/ViteByte/bestow/compare/v0.1.1...v0.1.2
[0.1.1]: https://codeberg.org/ViteByte/bestow/compare/v0.1.0...v0.1.1
[0.1.0]: https://codeberg.org/ViteByte/bestow/src/tag/v0.1.0
