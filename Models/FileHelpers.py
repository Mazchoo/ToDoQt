
import pandas as pd
from pathlib import Path
from os import listdir
from datetime import datetime
from typing import Dict, List

from PyQt5.QtGui import QStandardItemModel, QStandardItem

from Common.GenerateEncryption import decrypt_json_dict
from Models.CsvGeneration import create_updated_df, get_full_hash_path


def get_date_tuple_now():
    return eval(repr(datetime.now())[17:])


def get_hash_file_from_note_data(note_data: dict):
    return f"task_{note_data['id_number']}.hash_brown"


def delete_old_hash_browns(output_index: pd.Index, path: Path):
    hash_brown_files = [get_full_hash_path(path, f) for f in listdir(path / 'Hashbrowns') \
                        if Path(f).suffix == '.hash_brown']
    delete_hash_paths = [f for f in hash_brown_files if f.stem + f.suffix not in output_index]
    for hash_path in delete_hash_paths:
        hash_path.unlink()


def convert_list_to_note_data(model_list: QStandardItemModel):
    return [model_list.item(i).data() for i in range(model_list.rowCount())]


def try_decrypting_note(note_data: dict, file_name: Path, encrypt_fields: set, eval_fields: set):
    try:
        decrypted_note = decrypt_json_dict(note_data, file_name, encrypt_fields, eval_fields)
    except Exception:
        print("Error! Decryption failed")
        return None
    else:
        return decrypted_note


def load_content_from_csv(content_path: Path, encrypt_fields: set,
                          eval_fields: set) -> Dict[str, dict]:
    if content_path.exists():
        loaded_dicts = pd.read_csv(content_path, index_col=0).to_dict(orient='index')
    else:
        loaded_dicts = {}

    decrypted_notes = {}
    for file_name, note_data in loaded_dicts.items():
        file_path = get_full_hash_path(content_path.parent, file_name)
        if decrypted_note := try_decrypting_note(note_data, file_path, encrypt_fields, eval_fields):
            decrypted_notes[file_name] = decrypted_note

    return decrypted_notes


def load_projects_from_csv(path: Path) -> Dict[str, dict]:
    return {}


def add_new_item_to_model_list(model_list: QStandardItemModel, note_data: dict):
    new_item = QStandardItem(note_data['title'])
    new_item.setAccessibleDescription(note_data['description'])
    new_item.setData(note_data)
    model_list.appendRow(new_item)


def save_data_frame(save_path: Path, save_fields: List[str], encrypt_fields: List[str],
                    new_data: Dict[str, dict], original_data: Dict[str, dict]):
    if save_path.exists():
        original_df = pd.read_csv(save_path, index_col=0)
    else:
        original_df = pd.DataFrame(columns=save_fields)

    save_df = create_updated_df(original_df, new_data, original_data, save_path.parent, encrypt_fields)
    save_df.to_csv(save_path)

    return save_df
