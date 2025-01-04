
import os
from pathlib import Path
import pandas as pd
from PyQt5.QtGui import QStandardItemModel

from Common.QtModel import QtStaticModel
from Models.GlobalParams import (FIELDS_TO_EVAL, FIELDS_TO_ENCRYPT,
                                 STATUS_TYPES, TaskIdProvider, SAVED_TASKS_FILENAME)
from Models.NoteEntry import TaskEntry, update_note_data
from Models.NoteFileHelpers import (
    delete_old_hash_browns, get_hash_file_from_note_data,
    convert_list_to_note_data, load_notes_from_folder, add_new_item_to_model_list
)
from Models.CsvGeneration import create_updated_df

CWD = os.getcwd()


class ToDoModel(QtStaticModel):
    pending_list = QStandardItemModel
    in_progress_list = QStandardItemModel
    done_list = QStandardItemModel

    encrypt_fields = FIELDS_TO_ENCRYPT
    eval_fields = FIELDS_TO_EVAL

    def check_folder_path(self, rel_path: str):
        path = Path(f"{CWD}/{rel_path}")
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

        content_path = path / SAVED_TASKS_FILENAME
        if content_path.exists():
            original_df = pd.read_csv(content_path, index_col=0)
        else:
            columns = list(TaskEntry.model_fields.keys())
            original_df = pd.DataFrame(columns=columns)

        initial_file_data = load_notes_from_folder(path, self.encrypt_fields, self.eval_fields)

        final_df = create_updated_df(original_df, all_note_data, initial_file_data,
                                     path, self.encrypt_fields)
        final_df.to_csv(path / SAVED_TASKS_FILENAME)

        delete_old_hash_browns(final_df, path)

    def save_json_dict_into_model(self, note_data: dict):
        try:
            note_data = update_note_data(note_data)
            note_data = TaskEntry(**note_data).dict()

            assert (note_data['status'] in STATUS_TYPES)
            model_list = self.__getattribute__(note_data['status'])
        except Exception:
            print(f'json dict {note_data} cannot be read.')
            return

        TaskIdProvider.update_max_id(note_data['id_number'])
        add_new_item_to_model_list(model_list, note_data)

    def load_from_folder(self, rel_path: str):
        path = self.check_folder_path(rel_path)
        initial_file_data = load_notes_from_folder(path, self.encrypt_fields, self.eval_fields)

        sorted_keys = sorted(initial_file_data.keys())
        for key in sorted_keys:
            self.save_json_dict_into_model(initial_file_data[key])
