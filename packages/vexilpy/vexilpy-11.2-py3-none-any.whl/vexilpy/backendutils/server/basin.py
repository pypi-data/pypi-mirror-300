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

from ..server.standard import Server
from ..basin.object import BasinObject
from ..basin.getval import getval
from ..safety.handler import handle

class BasinServer(Server):
    @handle
    def __init__(self, name: str) -> None:
        basin: BasinObject = BasinObject(name)

        super().__init__(
            port=getval("port", basin, default=8000),
            directory=getval("directory", basin, default="./")
        )