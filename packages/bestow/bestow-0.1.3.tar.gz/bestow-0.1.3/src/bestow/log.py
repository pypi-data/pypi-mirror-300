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

"""
Provide simple logging utilities.

Proper logging makes it easier to convey information to the user, and
also helps with debugging.
"""

__all__ = [
    "LOG_LEVELS",
    "DEFAULT",
    "configure",
    "trace",
    "debug",
    "info",
    "warn",
    "error",
    "critical",
]

import sys
from typing import Any, NoReturn, TextIO

LOG_LEVELS = ("trace", "debug", "info", "warn", "error", "critical")
DEFAULT = "info"

# ANSI escape sequences.
CSI = "\x1B["
RED = CSI + "91m"
YELLOW = CSI + "93m"
RESET = CSI + "0m"

log_level = LOG_LEVELS.index(DEFAULT)
show_colour = True


def configure(level: str, colour: bool) -> None:
    """Configure the logging system."""
    global log_level, show_colour

    log_level = LOG_LEVELS.index(level)
    show_colour = colour

    debug(f"Log level {level}")


def _log(
    message: Any,
    *,
    level: str = "",
    use_colour: bool = False,
    colour: str = "",
    file: TextIO = sys.stdout,
    **kwargs: Any,
) -> None:
    # No-op if the set log level is higher than log call.
    if LOG_LEVELS.index(level) < log_level:
        return

    message = f"[{level}] {message}"

    # Display colours only if output is an interactive terminal.
    if show_colour and use_colour and file.isatty():
        message = colour + message + RESET

    # TODO: Utilise `logging` to keep persistent, detailed logs.
    print(message, **kwargs, file=file)


def trace(message: Any, **kwargs: Any) -> None:
    """
    Trace the execution flow of the program.

    This function is a no-op if the log level is higher than 0.
    """
    _log(message=message, level="trace", **kwargs)


def debug(message: Any, **kwargs: Any) -> None:
    """
    Display a debugging message.

    This function is a no-op if the log level is higher than 1.
    """
    _log(message=message, level="debug", **kwargs)


def info(message: Any, **kwargs: Any) -> None:
    """Display an informational message."""
    _log(message=message, level="info", **kwargs)


def warn(message: Any, *, use_colour: bool = True, **kwargs: Any) -> None:
    """Display a warning message."""
    _log(
        message,
        level="warn",
        use_colour=use_colour,
        colour=YELLOW,
        file=sys.stderr,
        **kwargs,
    )


def error(message: Any, *, use_colour: bool = True, **kwargs: Any) -> None:
    """Display an error message."""
    _log(
        message,
        level="error",
        use_colour=use_colour,
        colour=RED,
        file=sys.stderr,
        **kwargs,
    )


def critical(
    message: Any, *, use_colour: bool = True, exit_code: int = 1, **kwargs: Any
) -> NoReturn:
    """Display a critical error message and exit the program."""
    _log(
        message,
        level="critical",
        use_colour=use_colour,
        colour=RED,
        file=sys.stderr,
        **kwargs,
    )
    sys.exit(exit_code)
