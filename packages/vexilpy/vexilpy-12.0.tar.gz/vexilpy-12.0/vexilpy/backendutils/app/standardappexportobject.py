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

from typing import Any, Callable
from ..safety.handler import handle

from ..app.appobject import AppObject
from ..app.app import WebApp
from ..app.supportswith import SupportsWithKeyword

class StandardAppExportObject(SupportsWithKeyword):
    @handle
    def __init__(self, app_: WebApp, object_: Any = AppObject, *args: Any, **kwargs: Any) -> None:
        self.app: WebApp = app_
        self.name: str = "index" if self.app.fn.__name__.lower() == "base" else self.app.fn.__name__
        self.object: type[object_] = object_
        self.args: tuple[Any, ...] = args
        self.kwargs: dict[str, Any] = kwargs
        self.postb: Any = None

    def __invert__(self) -> Any:
        return self.open()

    @handle
    def open(self) -> Any:
        app_object: Any = self.object(self.name, self.app)
        app_object.exit()

        try: return handle(self.app.fn)(app_object, *self.args, **self.kwargs)
        finally: app_object.pass_to_server()

    @handle
    def init_postbuilding(self, type_: Callable) -> None:
        self.postb = type_(self.name, self.app)

    @handle
    def get_object_type(self) -> Any:
        return self.object

    @handle
    def get_app(self) -> WebApp:
        return self.app
    
def run_and_open(app: StandardAppExportObject, *args: Any, **kwargs: Any) -> Any:
    return app(*args, **kwargs).open()
