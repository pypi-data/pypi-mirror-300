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
from ..vexilpy.pwsh import pwsh

match sys.argv[1]:
    case "visit":
        match sys.argv[2]:
            case "vexilpy-github":
                pwsh(f"start https://github.com/elemenom/vexilpy/")

            case "vexilpy-pypi":
                pwsh(f"start https://pypi.org/project/vexilpy/")

            case "vexilpy-github-issues":
                pwsh(f"start https://github.com/elemenom/vexilpy/issues/")

            case "vexilpy-github-pr":
                pwsh(f"start https://github.com/elemenom/vexilpy/pulls/")

            case "vexilpy-github-pr-new":
                pwsh(f"start https://github.com/elemenom/vexilpy/compare/")

            case "vexilpy-github-insights":
                pwsh(f"start https://github.com/elemenom/vexilpy/pulse/")

            case "vexilpy-documentation":
                pwsh(f"start https://github.com/elemenom/vexilpy?tab=readme-ov-file#welcome-to-vexilpy/")

            case "vexilpy-license":
                pwsh(f"start https://github.com/elemenom/vexilpy/blob/main/LICENSE")

            case "author-github":
                pwsh(f"start https://github.com/elemenom/")

            case "author-pypi":
                pwsh(f"start https://pypi.org/user/elemenom/")

            case "vexilpy-github-download":
                pwsh(f"start https://github.com/elemenom/vexilpy/releases/")

    case "upgrade":
        pwsh("pip install vexilpy --upgrade")

    case "install":
        pwsh("pip install vexilpy")

    case "install-version":
        pwsh(f"pip install vexilpy=={sys.argv[2]}")

    case "info":
        pwsh("pip show vexilpy")

    case "uninstall":
        pwsh("pip uninstall vexilpy")

    case "documentation":
        import vexilpy

        print(vexilpy.__doc__)

    case "feedback":
        pwsh(f"start https://github.com/elemenom/vexilpy/issues/new/")

    case "license":
        print(__doc__)