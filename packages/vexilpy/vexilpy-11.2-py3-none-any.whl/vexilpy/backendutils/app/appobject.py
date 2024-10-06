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

import os

from typing import Optional, Any
from ..safety.handler import handle

from ..safety.logger import logger
from ..launcher.launch import launch
from ..app.supportswith import SupportsWithKeyword
from ..app.supportedtags import supported_tags
from ..script.ctrl import CTRLScript
from ..style.style import StyledAppAttachment

class AppObject(SupportsWithKeyword):
    @handle
    def __init__(self, name: Optional[str] = None, app: Any = None) -> None:
        super().__init__()

        from ..app.app import app as app_

        if app is None:
            logger().fatal("Please provide a parent app.")
            exit(1)

        self.server: Any = app.server
        self.name: str = name
        self.app: app_ = app
        self.style_: StyledAppAttachment | None = app.style
        self.new_stylesheet_path: str = f"{self.name}.css"
        self.ctrl: CTRLScript | None = None

        self.init_supported_tags(supported_tags)
        self.init_ctrlscript()

        self.on_run()

    @handle
    def on_run(self) -> None:
        logger().info("Please wait while we build your HTML file for you.")

        self.singular("<!DOCTYPE html>")
        self.singular("<html>")
        self.singular(f"<link rel=\"stylesheet\" href=\"{self.new_stylesheet_path}\">")
        self.singular(f"<script src=\"{self.name}.js\"></script>")

    @handle
    def init_ctrlscript(self) -> None:
        self.ctrl = CTRLScript(self.name)

    @handle
    def init_supported_tags(self, supported_tags_: list[str]) -> None:
        for tag in supported_tags_:
            exec(f"self.{tag} = lambda **args: self.tag({repr(tag)}, **args)", {"self": self})

    @handle
    def tag(self, type_: str, **kwargs: str) -> Any:
        from ..app.tagobject import TagObject

        final_kwargs = ""

        for key, value in list(kwargs.items()):
            final_kwargs += f"{key}=\"{value}\" "

        return TagObject(self.name, type_, self.app, final_kwargs)

    def __rshift__(self, other) -> None:
        self.singular(other)

    @handle
    def singular(self, ln: str) -> None:
        with open(f"{self.name}.html", "a") as file:
            file.write(ln + "\n")
            
    @handle
    def lorem(self) -> None:
        self.singular("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.")
        
    @handle
    def __exit__(self, *_) -> None:
        self.exit()

    @handle
    def exit(self) -> None:
        logger().info("Building has been finished successfully.")

    @handle
    def __getattr__(self, item) -> None:
        logger().error(f"Attribute '{item}' for 'SelfApp' does not exist. Skipping to next line.")

    @handle
    def pass_to_server(self) -> None:
        self.singular("</html>")

        if self.server is None:
            logger().fatal("Cannot pass vexilpy app script to server when no server was provided.")
            exit(1)

        logger().info(f"Passed '{self.name}' vexilpy app script to host '{type(self.server).__name__}'")

        if self.style is not None:
            logger().info(f"Passed stylesheet '{self.new_stylesheet_path}' to pebl script '{self.name}'.")

            self.style_.close()

        launch(self.server)

        logger().info("Continuing in pebl app to clear cache.")

        try: os.remove(f"{self.name}.html")
        except FileNotFoundError:
            logger().warn(f"Could not find '{self.name}', so it cannot be cleaned.")

        try: os.remove(self.ctrl.path)
        except FileNotFoundError:
            logger().warn(f"Could not find '{self.ctrl.path}', so it cannot be cleaned.")

        if self.style_ is not None:
            try: os.remove(self.new_stylesheet_path)
            except FileNotFoundError:
                logger().warn(f"Could not find '{self.new_stylesheet_path}', so it cannot be cleaned.")