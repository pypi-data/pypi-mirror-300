# Bestow

Simple and secure file transfer CLI.

[![Codeberg](https://img.shields.io/badge/Repository-Codeberg-blue?logo=codeberg&labelColor=white&style=plastic)](https://codeberg.org/ViteByte/bestow/)
[![CPython 3.10+](https://img.shields.io/badge/CPython-3.10_|_3.11_|_3.12_|_3.13-blue?style=plastic)](https://www.python.org/downloads/)
[![PyPI Version](https://img.shields.io/pypi/v/bestow?label=PyPI&color=blue&style=plastic)](https://pypi.org/project/bestow)
[![AGPLv3+ License](https://img.shields.io/pypi/l/bestow?label=License&color=blue&style=plastic)](https://codeberg.org/ViteByte/bestow/raw/branch/main/LICENSE)

## Table of Contents

- [Description](#description)
- [Features](#features)
- [Installation](#installation)
  - [Using uv](#using-uv)
  - [Using pip](#using-pip)
  - [Using Termux](#using-termux)
- [Usage](#usage)
    - [Sending a File](#sending-a-file)
    - [Receiving a File](#receiving-a-file)
- [License](#license)

## Description

This Python program facilitates fast encrypted file transfers over a TCP
connection. I made this project because I needed peace of mind when
sending data on an untrusted network.

## Features

- Straightforward command-line interface.
- Secured with modern encryption standards.
- Capable of handling large files efficiently.
- Speed benefits due to asynchronous design.
- Supports multiple client connections concurrently.

## Installation

This project supports CPython v3.10 and later. The latest version can be
installed at <https://python.org/download/>.

### Using uv

This is the recommended installation method because it isolates the
package environment from the system.

1. Install [`uv`](https://pypi.org/project/uv) if you haven't already:

```shell
python3 -m pip install --user uv
uv tool update-shell
```

2. Install the package:

```
uv tool install bestow
```

3. Update the package:

```
uv tool upgrade bestow
```

Make sure to restart the shell before using `bestow`.


### Using pip

:warning: This installation method is **not recommended**, as the
package will be installled in the global environment. This is not ideal
because it can lead to dependency conflicts or potentially break
packages needed by the system.

```
python3 -m pip install bestow
```

### Using Termux

If you have issues with the [recommended](#using-uv) install method
on [Termux](https://termux.dev/), you can build
[`PyNaCl`](https://pypi.org/project/pynacl/)
using the system installation of
[`libsodium`](https://doc.libsodium.org/).
The solution is was taken from a `PyNaCl`
[GitHub issue](https://github.com/pyca/pynacl/issues/483#issuecomment-608049721).

```shell
pkg install clang python libffi openssl libsodium
SODIUM_INSTALL=system python -m pip install pynacl
python3 install bestow
```

## Usage

The file transfer model involves two components: the server, who
provides the file, and the client, who receives the file. This model
ensures that the server can control who will receive the data and helps
to mitigate malicious actors.

### Sending a File

This will make it possible for a client to connect to the server's IP
address on a specific port (by default it is 50222).

```
bestow start file.txt
```

### Receiving a File

```
bestow connect 192.168.0.1
```

### License

This project is licensed under the GNU Affero General Public License
version 3.0 or later. See the
[LICENSE](https://codeberg.org/ViteByte/bestow/raw/branch/main/LICENSE)
file for more details.
