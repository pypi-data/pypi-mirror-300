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

import sys
from typing import Callable, Optional

from ..safety.logger import logger

def safe_input(prefix: Optional[str] = None, else_func: Optional[Callable] = None) -> str | None:
    if sys.stdin.closed:
        if else_func:
            else_func()

        else:
            logger().error("VexilPy tried to prompt the current terminal, but the connection was denied.")
            logger().hint("Stdin input stream has already been closed.")
            return
    else:
        return input(prefix or "")