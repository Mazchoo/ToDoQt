''' Loading and saving file helper functions '''
from pathlib import Path
from os import listdir, getcwd
from datetime import datetime
from typing import Dict, List, Tuple

import pandas as pd

from PyQt5.QtGui import QStandardItemModel, QStandardItem

from Common.GenerateEncryption import decrypt_json_dict
from Models.CsvGeneration import create_updated_df, get_full_hash_path

CWD = getcwd()


def get_date_tuple_now() -> Tuple[int, int, int, int, int, int, int]:
    ''' Get timestamp of right now according to local time year, month, day, hour, minute, second, ms '''
    now = datetime.now()
    return [now.year, now.month, now.day, now.hour, now.minute, now.second, now.microsecond]


def get_hash_file_from_task_data(task_data: dict):
    ''' Get name of hash brown file (encrypt key) for given task data '''
    return f"task_{task_data['id_number']}.hash_brown"


def get_hash_file_from_project_data(project_data: dict):
    ''' Get name of hash brown file (encrypt key) for given project data '''
    return f"project_{project_data['id_number']}.hash_brown"


def delete_old_hash_browns(output_index: pd.Index, path: Path):
    ''' Delete all hashbrown files that are no longer used '''
    hash_brown_files = [get_full_hash_path(path, f) for f in listdir(path / 'Hashbrowns')
                        if Path(f).suffix == '.hash_brown']
    delete_hash_paths = [f for f in hash_brown_files if f.stem + f.suffix not in output_index]
    for hash_path in delete_hash_paths:
        hash_path.unlink()


def convert_list_to_task_data(model_list: QStandardItemModel) -> List[dict]:
    ''' Convert Qt model list to a list of dict files for serialised '''
    return [model_list.item(i).data() for i in range(model_list.rowCount())]


def try_decrypting_dict(note_data: dict, file_name: Path, encrypt_fields: set, eval_fields: set):
    ''' Attempt to decrypt dictionary mapping to encrypted data '''
    try:
        decrypted_note = decrypt_json_dict(note_data, file_name, encrypt_fields, eval_fields)
    except Exception as e:
        print(f"Error! Decryption failed {e}")
        return None
    return decrypted_note


def load_content_from_csv(content_path: Path, encrypt_fields: List[str],
                          eval_fields: List[str]) -> Dict[str, dict]:
    ''' Load csv as encryption key file name matched to decrypted data '''
    if content_path.exists():
        loaded_dicts = pd.read_csv(content_path, index_col=0).to_dict(orient='index')
    else:
        loaded_dicts = {}

    decrypted_notes = {}
    for file_name, note_data in loaded_dicts.items():
        file_path = get_full_hash_path(content_path.parent, file_name)
        if decrypted_note := try_decrypting_dict(note_data, file_path, encrypt_fields, eval_fields):
            decrypted_notes[file_name] = decrypted_note

    return decrypted_notes


def add_new_item_to_model_list(model_list: QStandardItemModel, item_data: dict):
    ''' Add new item to item model '''
    new_item = QStandardItem(item_data['title'])
    new_item.setAccessibleDescription(item_data['description'])
    new_item.setData(item_data)
    model_list.appendRow(new_item)


def save_model_data(save_path: Path, save_fields: List[str], encrypt_fields: List[str],
                    new_data: Dict[str, dict], original_data: Dict[str, dict]):
    ''' Save dictionary data provided as encrypted csv '''
    if save_path.exists():
        original_df = pd.read_csv(save_path, index_col=0)
    else:
        original_df = pd.DataFrame(columns=save_fields)

    save_df = create_updated_df(original_df, new_data, original_data, save_path.parent, encrypt_fields)
    save_df.to_csv(save_path)

    return save_df


def check_folder_path(rel_path: str):
    ''' Raise expection if path is not valid folder '''
    path = Path(f"{CWD}/{rel_path}")
    if not path.exists() or not path.is_dir():
        raise FileNotFoundError(f"Invalid directory {path}")
    return path
