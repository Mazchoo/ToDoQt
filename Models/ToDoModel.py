
import os
from pathlib import Path
import pandas as pd
cwd = os.getcwd()

from PyQt5.QtGui import QStandardItemModel, QStandardItem

from Common.QtModel import QtStaticModel

from Models.GlobalParams import FIELDS_TO_EVAL, FIELDS_TO_ENCRYPT, STATUS_TYPES, NoteIdProvider
from Models.NoteEntry import NoteEntry, update_note_data
from Models.NoteFileHelpers import (
    delete_old_hash_browns, get_hash_file_from_note_data, turn_note_data_into_df,
    convert_list_to_note_data, load_notes_from_folder, get_all_new_notes,
    get_all_edited_notes, get_all_delete_notes, get_new_columns
)


class ToDoModel(QtStaticModel):
    pending_list = QStandardItemModel
    in_progress_list = QStandardItemModel
    done_list = QStandardItemModel
    encrypt_fields = FIELDS_TO_ENCRYPT
    eval_fields = FIELDS_TO_EVAL
    initial_file_data = {}

    def check_folder_path(self, rel_path: str):
        path = Path(f"{cwd}/{rel_path}")
        if not path.exists() or not path.is_dir():
            raise FileNotFoundError(f"Invalid directory {path}")
        return path

    def get_all_note_data(self):
        all_note_data = []
        for status in STATUS_TYPES:
            model_list = self.__getattribute__(status)
            all_note_data.extend(convert_list_to_note_data(model_list))

        return {get_hash_file_from_note_data(note): note for note in all_note_data}


    def save_to_folder(self, rel_path: str):
        path = self.check_folder_path(rel_path)
        
        all_note_data = self.get_all_note_data()
        edited_rows = get_all_edited_notes(all_note_data, self.initial_file_data)
        new_row_set = get_all_new_notes(all_note_data, self.initial_file_data)
        deleted_row_set = get_all_delete_notes(all_note_data, self.initial_file_data)

        final_df = pd.read_csv(path/'saved_content.csv', index_col=0)
        new_columns = get_new_columns(all_note_data, final_df.columns)
        new_rows = {k: v for k, v in all_note_data.items() if k in new_row_set}

        edited_rows_df = turn_note_data_into_df(edited_rows, path, self.encrypt_fields)
        new_rows_df = turn_note_data_into_df(new_rows, path, self.encrypt_fields)

        for col in new_columns:
            final_df[col] = None
        final_df.loc[edited_rows_df.index] = edited_rows_df
        final_df = pd.concat([final_df, new_rows_df])
        final_df.drop(deleted_row_set, inplace=True)

        final_df.sort_values(by=['id_number'])
        final_df.to_csv(path/'saved_content.csv')
        
        delete_old_hash_browns(final_df, path)
    
    def save_json_dict_into_model(self, json_dict: dict):
        try:
            json_dict = update_note_data(json_dict)
            json_dict = NoteEntry(**json_dict).dict()

            assert(json_dict['status'] in STATUS_TYPES)
            model_list = self.__getattribute__(json_dict['status'])
        except:
            print(f'json dict {json_dict} cannot be read.')
            return
        
        NoteIdProvider.update_max_id(json_dict['id_number'])
        new_item = QStandardItem(json_dict['title'])
        new_item.setAccessibleDescription(json_dict['description'])
        new_item.setData(json_dict)
        model_list.appendRow(new_item)
    
    def load_from_folder(self, rel_path: str):
        path = self.check_folder_path(rel_path)
        
        self.initial_file_data = load_notes_from_folder(path, self.encrypt_fields, self.eval_fields)
        sorted_keys = sorted(self.initial_file_data.keys())
        for key in sorted_keys:
            self.save_json_dict_into_model(self.initial_file_data[key])
