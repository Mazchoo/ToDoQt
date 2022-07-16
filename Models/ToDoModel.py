
import os
from pathlib import Path
import json
cwd = os.getcwd()

from PyQt5.QtGui import QStandardItemModel, QStandardItem

from Common.QtModel import QtStaticModel
from Common.GenerateEncryption import encrypt_dictionary_and_save_key, decrypt_json_dict


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


def convert_item_to_dict(save_item: QStandardItem, status_name: str):
    return {
        'title': save_item.text(),
        'description': save_item.accessibleDescription(),
        'status': status_name
    }


def save_dicts_as_json(json_dicts: list, status_name: str, path: Path, encrypt_fields: set):
    for i, json_dict in enumerate(json_dicts):
        file_name = path/f"{status_name}_{i}.json"

        try:
            encrypted_dict = encrypt_dictionary_and_save_key(json_dict, file_name, encrypt_fields)
        except:
            print("Warning! Decryption failed")
        else:
            json_dict = encrypted_dict
        
        with open(str(file_name), 'w') as f:
            json.dump(json_dict, f)


def convert_list_to_json_dicts(model_list: QStandardItemModel, status_name: str):
    output_dicts = []
    for i in range(model_list.rowCount()):
        output_dicts.append(convert_item_to_dict(model_list.item(i), status_name))
    return output_dicts


def try_decrypting_json_dict(json_dict: dict, file_name: Path, encrypt_fields: set):
    try:
        json_dict = decrypt_json_dict(json_dict, file_name, encrypt_fields)
    except:
        print("Error! Decryption failed")
        return None
    else:
        return json_dict


def load_jsons_from_folder(path: Path, encrypt_fields: set):
    all_jsons = {}
    for filename in os.listdir(path):
        if Path(filename).suffix == '.json':
            with open(str(path/filename), 'r') as f:
                all_jsons[filename] = json.load(f)

    decrypted_jsons = {}
    for filename, json_dict in all_jsons.items():
        file_path = path/filename
        if decrypted_dict := try_decrypting_json_dict(json_dict, file_path, encrypt_fields):
            decrypted_jsons[filename] = decrypted_dict

    sorted_list = sorted([filename for filename in decrypted_jsons.keys()])
    return [decrypted_jsons[filename] for filename in sorted_list]


def json_dict_is_valid_item(json_dict: dict):
    if 'title' not in json_dict:
        return False
    elif 'description' not in json_dict:
        return False
    elif 'status' not in json_dict:
        return False
    elif not hasattr(ToDoModel, json_dict['status']):
        return False
    else:
        return True


class ToDoModel(QtStaticModel):
    pending_list = QStandardItemModel
    in_progress_list = QStandardItemModel
    done_list = QStandardItemModel
    encrypt_fields = {'title', 'description'}

    def check_folder_path(self, rel_path: str):
        path = Path(f"{cwd}/{rel_path}")
        if not path.exists() or not path.is_dir():
            raise FileNotFoundError(f"Invalid directory {path}")
        return path

    def save_list_as_jsons(self, status_name: str, path: Path):
        model_list = self.__getattribute__(status_name)
        pending_dicts = convert_list_to_json_dicts(model_list, status_name)
        save_dicts_as_json(pending_dicts, status_name, path, self.encrypt_fields)

    def save_to_folder(self, rel_path: str):
        path = self.check_folder_path(rel_path)

        delete_all_jsons_in_folder(path)

        self.save_list_as_jsons('pending_list', path)
        self.save_list_as_jsons('in_progress_list', path)
        self.save_list_as_jsons('done_list', path)
    
    def save_json_dict_into_model(self, json_dict: dict):
        if not json_dict_is_valid_item(json_dict):
            return

        model_list = self.__getattribute__(json_dict['status'])
        if isinstance(model_list, QStandardItemModel):
            new_item = QStandardItem(json_dict['title'])
            new_item.setAccessibleDescription(json_dict['description'])
            model_list.appendRow(new_item)
    
    def load_from_folder(self, rel_path: str):
        path = self.check_folder_path(rel_path)
        
        for json_dict in load_jsons_from_folder(path, self.encrypt_fields):
            self.save_json_dict_into_model(json_dict)
