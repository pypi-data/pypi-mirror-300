from random import randint
from typing import Optional, Any

from ..safety.handler import handle
from ..safety.logger import logger

@handle
class InclusionMap:
    def __init__(self, /, __id__: Optional[str] = None, **inclusions: Any) -> None:
        self.id: str = __id__ or str(randint(0, 999999))

        self.inclusions: dict[str, Any] = inclusions

        logger().info(f"Created inclusion map {self.id}")

@handle
class SafeInclusionMap:
    def __init__(self, attributes: list[str], classes: list[Any], __id__: Optional[str] = None) -> None:
        self.id: str = __id__ or str(randint(0, 999999))

        self.attributes: list[str] = attributes
        self.classes: list[Any] = classes

        logger().info(f"Created inclusion map {self.id}")