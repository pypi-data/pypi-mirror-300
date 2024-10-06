from importlib import import_module
from typing import Any

from ..safety.handler import handle

from ..safety.logger import logger

@handle
def batch_import(sector: str, name: str) -> Any:
    root: Any = import_module(f"..stock.{sector}.{name}", __package__)

    return root

@handle
def stock_import(sector: str, name: str, material: str) -> Any:
    try:
        return getattr(batch_import(sector, name), material)
    except Exception as err:
        logger().error(f"An error occurred in a stock module: {sector}.{name}.{material}")
        logger().error(f"Error details: {type(err).__name__} in {err.__traceback__.tb_frame.f_code.co_name}")
