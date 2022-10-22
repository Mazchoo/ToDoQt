
import os
from pathlib import Path
import pandas as pd
cwd = os.getcwd()

from PyQt5.QtGui import QStandardItemModel, QStandardItem

from Common.QtModel import QtStaticModel
from Common.GenerateEncryption import encrypt_dictionary_and_save_key, decrypt_json_dict

from Models.GlobalParams import FIELDS_TO_EVAL, FIELDS_TO_ENCRYPT, STATUS_TYPES
from Models.NoteEntry import NoteEntry, update_note_data


def delete_all_jsons_in_folder(path):
    for filename in os.listdir(path):   
        delete_path = path/filename
        if delete_path.suffix == '.json':
            delete_path.unlink()


def delete_all_hash_browns_in_folder(path):
    for filename in os.listdir(path):   
        delete_path = path/filename
        if delete_path.suffix == '.hash_brown':
            delete_path.unlink()


def turn_json_dicts_into_df(json_dicts: list, status_name: str, path: Path, encrypt_fields: set):
    encrypted_dicts = {}
    for i, json_dict in enumerate(json_dicts):
        file_name = f"{status_name}_{i}.json"
        file_path = path/file_name

        try:
            encrypted_dict = encrypt_dictionary_and_save_key(json_dict, file_path, encrypt_fields)
        except:
            print(f"Error! Encryption failed {file_name}")
        else:
            encrypted_dicts[file_name] = encrypted_dict

    return pd.DataFrame.from_dict(encrypted_dicts, orient='index')


def convert_list_to_json_dicts(model_list: QStandardItemModel):
    return [model_list.item(i).data() for i in range(model_list.rowCount())]


def try_decrypting_json_dict(json_dict: dict, file_name: Path, encrypt_fields: set, eval_fields: set):
    try:
        json_dict = decrypt_json_dict(json_dict, file_name, encrypt_fields, eval_fields)
    except:
        print("Error! Decryption failed")
        return None
    else:
        return json_dict


def load_jsons_from_folder(path: Path, encrypt_fields: set, eval_fields: set):
    all_jsons = pd.read_csv(path/'saved_content.csv', index_col=0).to_dict(orient='index')

    decrypted_jsons = {}
    for filename, json_dict in all_jsons.items():
        file_path = path/filename
        if decrypted_dict := try_decrypting_json_dict(json_dict, file_path, encrypt_fields, eval_fields):
            decrypted_jsons[filename] = decrypted_dict

    sorted_list = sorted([filename for filename in decrypted_jsons.keys()])
    return [decrypted_jsons[filename] for filename in sorted_list]


class ToDoModel(QtStaticModel):
    pending_list = QStandardItemModel
    in_progress_list = QStandardItemModel
    done_list = QStandardItemModel
    encrypt_fields = FIELDS_TO_ENCRYPT
    eval_fields = FIELDS_TO_EVAL

    def check_folder_path(self, rel_path: str):
        path = Path(f"{cwd}/{rel_path}")
        if not path.exists() or not path.is_dir():
            raise FileNotFoundError(f"Invalid directory {path}")
        return path

    def save_list_as_jsons(self, status_name: str, path: Path):
        model_list = self.__getattribute__(status_name)
        pending_dicts = convert_list_to_json_dicts(model_list)
        return turn_json_dicts_into_df(pending_dicts, status_name, path, self.encrypt_fields)

    def save_to_folder(self, rel_path: str):
        path = self.check_folder_path(rel_path)
        output_dfs = [self.save_list_as_jsons(status, path) for status in STATUS_TYPES]

        new_df = pd.concat(output_dfs)
        new_df.sort_values(by=['id_number'])
        new_df.to_csv(path/'saved_content.csv')
    
    def save_json_dict_into_model(self, json_dict: dict):
        try:
            json_dict = update_note_data(json_dict)
            json_dict = NoteEntry(**json_dict).dict()

            assert(json_dict['status'] in STATUS_TYPES)
            model_list = self.__getattribute__(json_dict['status'])
        except:
            print(f'json dict {json_dict} cannot be read.')
            return
        
        new_item = QStandardItem(json_dict['title'])
        new_item.setAccessibleDescription(json_dict['description'])
        new_item.setData(json_dict)
        model_list.appendRow(new_item)
    
    def load_from_folder(self, rel_path: str):
        path = self.check_folder_path(rel_path)
        
        for json_dict in load_jsons_from_folder(path, self.encrypt_fields, self.eval_fields):
            self.save_json_dict_into_model(json_dict)

# ToDo - Data would be better stored in a csv and only check items that have a new id
