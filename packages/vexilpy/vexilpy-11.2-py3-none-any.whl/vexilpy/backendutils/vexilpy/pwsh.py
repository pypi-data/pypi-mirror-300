from subprocess import run
from ..safety.handler import handle

@handle
def pwsh(cmd: str) -> None:
    run(["powershell", "-Command", cmd])