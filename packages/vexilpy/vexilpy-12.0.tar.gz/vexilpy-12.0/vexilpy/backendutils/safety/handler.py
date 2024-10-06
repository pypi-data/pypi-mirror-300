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
from functools import wraps
from typing import Callable, Any

def handle(fn: Callable) -> Callable:
    @wraps(fn)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        from ..safety.logger import logger
        from ..safety.safe_input import safe_input
        
        try:
            result: Any = fn(*args, **kwargs)
            return result

        except KeyboardInterrupt:
            try:
                logger().warning("Abandoning VexilPy while it's still running may cause currently open\n"
                               "servers to continue to take up their address in your memory.\n"
                               "Please exit the program safely or press CTRL+C/CTRL+D again.\n"
                               "Press ENTER to cancel this exit attempt."
                )
                safe_input()

            except KeyboardInterrupt:
                logger().fatal("Exiting program... KeyboardInterrupt")
                exit(0)

            return
        
        except AssertionError as err:
            file_name = fn.__module__.split('.')[-1] + '.py'
            func_name = fn.__name__
            logger().fatal(f"VexilPy component '{file_name}', function/class '{func_name}' asserted requirements that were not met.")
            logger().hint("Please ensure all necessary dependencies are installed and configured correctly.")
            
            exit(1)

        except Exception as err:
            from ... import verbose

            if verbose:
                logger().fatal(f"An error was caught but the handler is offline. Recovery process aborted.")
                logger().hint(f"This might be because the current running VexilPy instance is Verbose.")

                raise err

            else:
                logger().error(f"VexilPy encountered an error `{type(err).__name__}` in function `{fn.__name__}`,")
                logger().hint(f"but the system managed to recover.")
                logger().hint(f"Use `python {" ".join(sys.argv)} --Verbose` to disable error recovery.")

                return

    return wrapper