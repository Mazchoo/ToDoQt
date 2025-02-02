
'''
    Convert a .ui from QDesigner into the equivalent Python .py layout file

    This file requires pyuic5 to be installed in the current environment:
        pip install pyuic5-tool
'''

import os
from pathlib import Path


UI_FOLDER = f"{os.getcwd()}/UI"


def convertUiFileToPython(input_file: str, output_name: str):
    ''' Convert given .ui from QDesigner into a Python ui file .py '''
    ui_path = Path(f"{UI_FOLDER}/{input_file}")

    if not ui_path.exists():
        raise FileNotFoundError(f"UI file {input_file} does not exist.")
    if ui_path.suffix != ".ui":
        raise ValueError(f"Expected {input_file} to be ui file.")

    command = f"pyuic5 -x {ui_path} -o {UI_FOLDER}/{output_name}"
    os.system(command)


if __name__ == '__main__':
    convertUiFileToPython("ToDoApp.ui", "ToDoLayout.py")
