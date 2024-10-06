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
from typing import Optional, Any

from ..safety.logger import logger
from ..style.attribute import StyleAttribute
from ..safety.handler import handle

from .inclusion import InclusionMap, SafeInclusionMap

class StyledAppAttachment:
    @handle
    def __init__(self, path: Optional[str] = None) -> None:
        self.path: str | None = path
        self.write_later: str = ""
        self.attributes: list[StyleAttribute] = []

    @handle
    def close(self, path: Optional[str] = None) -> None:
        self.path = path or self.path

        for attribute in self.attributes:
            self._write_attrib_contents(attribute)

        self._init_file(path, self.write_later)

    def apply(self, inc_map: InclusionMap) -> None:
        logger().info(f"Created inclusion map {inc_map.id}")

        for attribute, cls in list(inc_map.inclusions.items()):
            self._add_attribute(attribute).include(cls)

        logger().info(f"Inclusion map {inc_map.id} applied to {self.path}")

    def safe_apply(self, inc_map: SafeInclusionMap) -> None:
        logger().info(f"Created inclusion map {inc_map.id}")

        for attribute, cls in zip(inc_map.attributes, inc_map.classes):
            self._add_attribute(attribute).include(cls)

        logger().info(f"Inclusion map {inc_map.id} applied to {self.path}")

    @handle
    def _init_file(self, path: Optional[str] = None, write: Optional[str] = None) -> None:
        with open((self.path or (path or "index.css")), "w") as file:
            file.write(write or "")

    @handle
    def _add_attribute(self, key: Optional[str] = None) -> StyleAttribute:
        key = key or "base"
        key = "html" if key.lower() == "base" else key

        attribute: StyleAttribute = StyleAttribute(self, key or "html")
        self.attributes.append(attribute)

        return attribute

    #

    @handle
    def type_selector(self, key: str) -> StyleAttribute:
        return self._add_attribute(key)

    @handle
    def id_selector(self, key: str) -> StyleAttribute:
        return self._add_attribute(f"#{key}")

    @handle
    def class_selector(self, key: str) -> StyleAttribute:
        return self._add_attribute(f".{key}")

    @handle
    def universal_selector(self) -> StyleAttribute:
        return self._add_attribute("*")

    @handle
    def attribute_selector(self, key: str, **kwargs) -> StyleAttribute:
        final_kwargs = ""

        for key, value in list(kwargs.items()):
            final_kwargs += f"{key}=\"{value}\" "

        return self._add_attribute(f"{key}[{final_kwargs}]")

    @handle
    def pseudo_class_selector(self, key: str, attribute: str) -> StyleAttribute:
        return self._add_attribute(f"{key}:{attribute}")

    @handle
    def pseudo_element_selector(self, key: str, attribute: str) -> StyleAttribute:
        return self._add_attribute(f"{key}::{attribute}")

    @handle
    def child_selector(self, key: str, child: str) -> StyleAttribute:
        return self._add_attribute(f"{key} > {child}")

    @handle
    def descendant_selector(self, ancestor: str, descendant: str) -> StyleAttribute:
        return self._add_attribute(f"{ancestor} {descendant}")

    @handle
    def sibling_selector(self, element: str, sibling: str) -> StyleAttribute:
        return self._add_attribute(f"{element} + {sibling}")

    @handle
    def general_sibling_selector(self, element: str, sibling: str) -> StyleAttribute:
        return self._add_attribute(f"{element} ~ {sibling}")

    @handle
    def grouping_selector(self, *keys: str) -> StyleAttribute:
        return self._add_attribute(f"{", ".join(keys)}")

    @handle
    def type_selector(self, key: str) -> StyleAttribute:
        return self._add_attribute(f"{key}")

    #

    @handle
    def _write_attrib_contents(self, attribute: StyleAttribute) -> None:
        self.write_later += f"{attribute.get_written()}\n"

    @handle
    def set_path(self, path: str) -> None:
        self.path = path