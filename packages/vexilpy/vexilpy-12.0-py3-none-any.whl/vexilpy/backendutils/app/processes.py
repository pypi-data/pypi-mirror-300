from typing import Callable, Any

class ExecMethod:
    def __init__(self, cls: Callable, *args: Any, **kwargs: Any) -> None:
        self.__cls__ = cls
        self.obj = cls(*args, **kwargs)

    def __action__(self, *_) -> None:
        ...

    def __wrapper__(self, other: tuple[Any, ...]) -> Any:
        return self.obj.__action__(*other)

def m(cls: Any) -> ExecMethod:
    return ExecMethod(cls)