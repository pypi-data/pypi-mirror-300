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

from ..safety.handler import handle
from ..safety.safe_input import safe_input
from ..vexilpy.vexilpyserverorrelated import VexilPyServerOrRelatedObjects

@handle
def launch(server: VexilPyServerOrRelatedObjects) -> VexilPyServerOrRelatedObjects:
    try:
        server.open()
        safe_input("\033[1;93mPress enter to exit your VexilPy server...\n\033[0m")

    finally:
        server.close()

    return server