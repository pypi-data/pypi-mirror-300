import inspect, os

from typing import Optional, Self

from ..app.standardappexportobject import StandardAppExportObject
from ..app.blankslateobject import new
from ..app.app import WebApp
from ..app.supportswith import SupportsWithKeyword

class RepositoryObject(SupportsWithKeyword):
    def __init__(self, name: Optional[str] = None) -> None:
        self.pages: list[WebApp] = []
        
        self.name: str | None = None

    def __enter__(self) -> Self:
        # Get the frame of the caller
        frame = inspect.currentframe().f_back
        
        # Get the source code of the line containing the with statement
        source_line = inspect.getframeinfo(frame).code_context[0].strip()
        
        # Extract the "as name" part if it exists
        if "as" in source_line:
            self.name = source_line.split("as")[-1].strip().split(":")[0].strip()
        else:
            self.name = None
            
        self.init_directory()
            
        return self
        
    def init_directory(self) -> Self:
        os.mkdir(self.as_name)
        
        return self
    
    def __exit__(self, *_, **__) -> None:
        self.destroy_directory()
        
    def destroy_directory(self) -> Self:
        os.rmdir(self.name)
        
        return self
    
    def __truediv__(self, app: StandardAppExportObject) -> StandardAppExportObject:
        self.pages.append(app.app)
        
        return app