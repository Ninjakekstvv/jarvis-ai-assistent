import os
import subprocess
from pathlib import Path

def open_program(program_name):
    program_name = program_name.lower().strip()

    start_menu = [
        Path(os.environ["ProgramData"]) / "Microsoft/Windows/Start Menu/Programs",
        Path(os.environ["APPDATA"]) / "Microsoft/Windows/Start Menu/Programs",
    ]

    for folder in start_menu:
        for shortcut in folder.rglob("*.lnk"):
            if program_name in shortcut.stem.lower():
                os.startfile(shortcut)
                return True

    return False