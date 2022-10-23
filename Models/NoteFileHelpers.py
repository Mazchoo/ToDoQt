
import pandas as pd
from pathlib import Path
from os import listdir

from PyQt5.QtGui import QStandardItemModel

from Common.GenerateEncryption import encrypt_dictionary_and_save_key, decrypt_json_dict


def get_hash_file_from_note_data(note_data: dict):
    return f"note_{note_data['id_number']}.hash_brown"


def get_full_hash_path(save_folder: Path, file_name: str):
    return save_folder/'Hashbrowns'/file_name


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
        except:
            print(f"Error! Encryption failed {file_name}")
        else:
            encrypted_notes[file_name] = encrypted_note

    return pd.DataFrame.from_dict(encrypted_notes, orient='index')


def convert_list_to_note_data(model_list: QStandardItemModel):
    return [model_list.item(i).data() for i in range(model_list.rowCount())]


def try_decrypting_note(note_data: dict, file_name: Path, encrypt_fields: set, eval_fields: set):
    try:
        decrypted_note = decrypt_json_dict(note_data, file_name, encrypt_fields, eval_fields)
    except:
        print("Error! Decryption failed")
        return None
    else:
        return decrypted_note


def load_notes_from_folder(path: Path, encrypt_fields: set, eval_fields: set):
    loaded_dicts = pd.read_csv(path/'saved_content.csv', index_col=0).to_dict(orient='index')

    decrypted_notes = {}
    for file_name, note_data in loaded_dicts.items():
        file_path = get_full_hash_path(path, file_name)
        if decrypted_note := try_decrypting_note(note_data, file_path, encrypt_fields, eval_fields):
            decrypted_notes[file_name] = decrypted_note

    return decrypted_notes


def get_all_new_notes(all_note_data: dict, initial_data: dict):
    all_previous_keys = initial_data.keys()
    all_current_keys = set(all_note_data.keys())
    return all_current_keys.difference(all_previous_keys)


def get_all_edited_notes(all_note_data: dict, initial_data: dict):
    edited_notes = {}
    for key, json_dict in all_note_data.items():
        if key in initial_data and initial_data[key] != json_dict:
            edited_notes[key] = json_dict

    return edited_notes


def get_all_delete_notes(all_note_data: dict, initial_data: dict):
    all_previous_keys = set(initial_data.keys())
    all_current_keys = all_note_data.keys()
    return all_previous_keys.difference(all_current_keys)


def get_new_columns(all_note_data: dict, current_cols: list):
    new_columns = {}
    if all_note_data:
        current_cols_set = set(current_cols)
        first_note = list(all_note_data.values())[0]
        current_cols_set.difference(first_note.keys())
    return new_columns
