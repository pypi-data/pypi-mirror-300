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

import os, yaml

from typing import Any

from ..safety.handler import handle
from ..safety.logger import logger

@handle
def load_yaml_config(path: str) -> Any:
    if os.path.exists(path):
        with open(path) as file:
            config: Any = yaml.safe_load(file)

        return config

    else:
        logger().fatal(f"yaml: Configuration file '{path}' not found.")
        exit(1)