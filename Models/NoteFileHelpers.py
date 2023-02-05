
import pandas as pd
from pathlib import Path
from os import listdir

from PyQt5.QtGui import QStandardItemModel, QStandardItem

from Common.GenerateEncryption import encrypt_dictionary_and_save_key, decrypt_json_dict


def get_hash_file_from_note_data(note_data: dict):
    return f"note_{note_data['id_number']}.hash_brown"


def get_full_hash_path(save_folder: Path, file_name: str):
    return save_folder / 'Hashbrowns' / file_name


def delete_old_hash_browns(output_df: pd.DataFrame, path: Path):
    hash_brown_files = [get_full_hash_path(path, f) for f in listdir(path) if Path(f).suffix == '.hash_brown']
    delete_hash_paths = [f for f in hash_brown_files if f.stem + f.suffix not in output_df.index]
    for hash_path in delete_hash_paths:
        hash_path.unlink()


def turn_note_data_into_df(note_data_dict: dict, path: Path, encrypt_fields: set):
    encrypted_notes = {}
    for file_name, note_data in note_data_dict.items():
        file_path = get_full_hash_path(path, file_name)

        try:
            encrypted_note = encrypt_dictionary_and_save_key(note_data, file_path, encrypt_fields)
        except Exception:
            print(f"Error! Encryption failed {file_name}")
        else:
            encrypted_notes[file_name] = encrypted_note

    return pd.DataFrame.from_dict(encrypted_notes, orient='index')


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


def load_notes_from_folder(path: Path, encrypt_fields: set, eval_fields: set):
    loaded_dicts = pd.read_csv(path / 'saved_content.csv', index_col=0).to_dict(orient='index')

    decrypted_notes = {}
    for file_name, note_data in loaded_dicts.items():
        file_path = get_full_hash_path(path, file_name)
        if decrypted_note := try_decrypting_note(note_data, file_path, encrypt_fields, eval_fields):
            decrypted_notes[file_name] = decrypted_note

    return decrypted_notes


def add_new_item_to_model_list(model_list: QStandardItemModel, note_data: dict):
    new_item = QStandardItem(note_data['title'])
    new_item.setAccessibleDescription(note_data['description'])
    new_item.setData(note_data)
    model_list.appendRow(new_item)
