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

from tkinter import Tk, Label, Entry, Button
from tkinter.messagebox import showerror, showinfo
from typing import Any, Optional
from ..vexilpy.msie import pwsh
from ..safety.logger import logger

def run_process(text: str, logger: Any, id_: Optional[str] = None) -> None:
    if text == "":
        showerror("Error", "Please enter a value. Trying to specify a FilePath in the terminal? Try running '$$TERMINAL'. (without quotes)")
        return

    text_upper = text.upper()
    if text_upper == "$$TERMINAL":
        print("/!\\ Continuing in a terminal does not support '$$' commands, '>' commands, '%' commands, 'vexilpy://' sites, and custom commands like 'vexilpyping', 'exit' or 'vexilpyhelp'.")
        text = ""

    elif text_upper == "$$HELP":
        text = ">helpvexilpy"

    elif text_upper == "$$PING":
        text = ">pingvexilpy"

    elif text_upper == "$$EXIT":
        text = ">exit"

    elif text_upper == "$$INDEX":
        text = "vexilpy://app/index.py"

    elif text_upper == "$$-8000":
        text = "vexilpy://8000"

    elif text_upper == "$$-24001":
        text = "vexilpy://24001"

    if text.startswith("vexilpy://app/"):
        pwsh(f"python {text.removeprefix('vexilpy://app/')}.py")

    elif text.startswith("vexilpy://"):
        url = f"http://localhost:{text.removeprefix('vexilpy://')}/"
        pwsh(f"start {url}")

    elif text.strip(">") in {"exit", "%exit"}:
        logger().info("Exited VexilPy RUNGUI.")

    elif text.strip(">") in {"help", "%help"}:
        print("> Looking for help regarding VexilPy and VexilPy RUNGUI? Try '$$HELP'.")

    elif text.strip(">") in {"helpvexilpy", "%helpvexilpy"}:
        showinfo("Help", r"$$EXIT, %exit, >exit - exit the GUI and end the program. $$PING, %pingvexilpy - Ping the terminal from this VexilPy RUNGUI. $$TERMINAL - continue in terminal. See the 'README.md' file or run 'import vexilpy; print(vexilpy.MyVexilPy.help())' in a Python command line interface for more help.")

    elif text.strip(">") in {"pingvexilpy", "%pingvexilpy"}:
        logger().info(f"Ping received from VexilPy RUNGUI 'id={id_ or 'none (unnamed)'}'.")

    elif text.startswith(">") or text.startswith("%"):
        pwsh(text.strip(">") if text.strip(">") != text else text.removeprefix("%"))

    else:
        pwsh(f"start {text}")

def run_gui(id: Optional[str] = None) -> None:
    root = Tk()
    root.title("Run using VexilPy")
    root.geometry("400x150")
    root.resizable(False, False)

    Label(root, text="Run a new process using VexilPy").pack()
    entry = Entry(root, width=80)
    entry.pack(padx=10, pady=10)
    Button(root, text="Submit", command=lambda:\
        run_process(entry.get(), logger, id)).pack(pady=10)

    logger().info("Completed dist; launch sequence initiated.")
    root.mainloop()