
'''
    Instead of loading the UI file directly in, we can get a .py file
    that is no longer an intermediate form of the layout.

    This file requires pyuic5 to be installed in the current environment:
        pip install pyuic5-tool
'''

import os
from pathlib import Path


UI_FOLDER = f"{os.getcwd()}/UI"

def convertUiFileToPython(input_file, output_name):
    ui_path = Path(f"{UI_FOLDER}/{input_file}")

    if not ui_path.exists():
        raise FileNotFoundError(f"UI file {input_file} does not exist.")
    if ui_path.suffix != ".ui":
        raise ValueError(f"Expected {input_file} to be ui file.")

    command = f"pyuic5 -x {ui_path} -o {UI_FOLDER}/{output_name}"
    os.system(command)


if __name__ == '__main__':
    input_file = "ToDoApp.ui"
    output_name = "ToDoLayout.py"
    convertUiFileToPython(input_file, output_name)
