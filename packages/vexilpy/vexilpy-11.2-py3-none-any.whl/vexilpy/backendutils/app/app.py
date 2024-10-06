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

from typing import Optional, Callable
from ..safety.handler import handle
from ..safety.logger import logger
from ..vexilpy.vexilpyserverorrelated import VexilPyServerOrRelatedObjects
from ..app.appobject import AppObject
from ..app.supportswith import SupportsWithKeyword
from ..app.blankslateobject import new

class WebApp(SupportsWithKeyword):
    @handle
    def __init__(self, server: Optional[VexilPyServerOrRelatedObjects] = None, style_path: Optional[str] = None) -> None:
        from ..style.style import StyledAppAttachment

        self.style = new("StyledAppAttachmentWithBackAttribute", (StyledAppAttachment,),
            back = lambda _:\
                self
        )(style_path)

        super().__init__()

        self.server: VexilPyServerOrRelatedObjects | None = server
        self.fn: Callable | None = None

        self._init_root()

    def __call__(self, *_) -> Callable:
        logger().error("WebApp object cannot be called directly. Maybe you forgot to export it?")
        logger().hint("Incase this is true, we'll export this WebApp automatically using export.standard.")

        return self.export_standard(_[0])

    @handle
    def _init_root(self) -> None:
        self.export = new("export", (), # Export methods here:
            __call__=self.export_call_method,
            standard=self.export_standard,
            void=self.export_void,
            void_without_lambda=self.export_voidnolambda,
            direct=self.export_direct,
            dont_pass=self.export_nopass,
            __getattr__=self.export_getattr
        )()

    @handle
    def export_call_method(self, *_) -> Callable:
        logger().error("'WebApp.export' does not accept arguments.")
        logger().hint("Maybe you forgot to add an export method (standard, void, etc.)?")
        logger().hint("Incase this is true, export.standard will be used to prevent unwanted behaviour.")

        return self.export_standard(_[0])

    @handle
    def export_getattr(self, attr: str, *_) -> Callable:
        logger().error(f"'{attr}' is not a valid export method.")
        logger().hint(f"See the documentation for a list of valid export methods.")
        logger().hint("export.standard will be used to prevent unwanted behaviour.")

        return self.export_standard

    @handle
    def export_standard(self, fn: Callable) -> Callable:
        self.fn = handle(fn)

        from ..app.standardappexportobject import StandardAppExportObject

        return lambda *args, **kwargs:\
            StandardAppExportObject(self, AppObject, *args, **kwargs)

    @handle
    def export_void(self, fn: Callable) -> Callable:
        return lambda *args, **kwargs:\
            handle(fn)(*args, **kwargs)

    @handle
    def export_voidnolambda(self, fn: Callable) -> None:
        return handle(fn)

    @handle
    def export_direct(self, fn: Callable) -> None:
        app_object: AppObject = AppObject(fn.__name__, self)
        app_object.exit()

        try: return handle(fn)(app_object)
        finally: app_object.pass_to_server()

    @handle
    def export_nopass(self, fn: Callable) -> None:
        app_object: AppObject = AppObject(fn.__name__, self)
        app_object.exit()

        return handle(fn)(app_object)

@handle
def app(server: Optional[VexilPyServerOrRelatedObjects] = None, style_path: Optional[str] = None) -> WebApp:
    return WebApp(server, style_path)