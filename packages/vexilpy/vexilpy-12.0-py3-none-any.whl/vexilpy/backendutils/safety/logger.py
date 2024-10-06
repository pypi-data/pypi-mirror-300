"""
This file is part of VexilPy (elemenom/vexilpy).

VexilPy is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

VexilPy is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with VexilPy. If not, see <https://www.gnu.org/licenses/>.
"""

import logging
from typing import Any, Callable

from ..safety.uselessobject import UselessObject
from ..safety.handler import handle

logger_literal: Any = NotImplementedError

@handle
def logger() -> Any:
    if not logger_literal:
        from ..app.blankslateobject import new

        print("error: vexilpy tried to interact with the logger, but access was denied.")
        print("info: logger has been either destroyed, or not yet initialised.")
        print("info: attempting to retrieve log type and contents (marked as '--pseudo-logger'):")

        return new("UselessObjectWithPrinter", (UselessObject,),
            __getattribute__ = \
                lambda item:\
                    lambda value:\
                        print(f"--pseudo-logger {item.lower()}: {value}")
        )()

    return logger_literal

def _add_level(logger_: Any, level: int, name: str) -> None:
    logging.addLevelName(level, name)
    
    setattr(logger_.__class__, name.lower(), 
        lambda self, message, *args, **kwargs:
            self._log(level, message, args, **kwargs) if self.isEnabledFor(level) else None
    )

def init_logger(logger_: Any) -> None:
    global logger_literal

    logger_literal = logger_
    
    _add_level(logger_literal, 25, "HINT")