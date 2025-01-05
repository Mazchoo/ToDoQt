
import os
from pathlib import Path
import pandas as pd
from PyQt5.QtGui import QStandardItemModel

from Common.QtModel import QtStaticModel
from Models.GlobalParams import (TASK_FIELDS_APPLY_EVAL, TASK_FIELDS_TO_ENCRYPT,
                                 STATUS_TYPES, SAVED_TASKS_FILENAME)
from Models.TaskEntry import TaskEntry, update_note_data, TaskIdProvider
from Models.FileHelpers import (
    delete_old_hash_browns, get_hash_file_from_note_data,
    convert_list_to_note_data, load_tasks_from_csv, add_new_item_to_model_list,
    load_projects_from_csv
)
from Models.CsvGeneration import create_updated_df
from Models.PandasTable import PandasModel

CWD = os.getcwd()


class ToDoModel(QtStaticModel):
    pending_list = QStandardItemModel
    in_progress_list = QStandardItemModel
    done_list = QStandardItemModel
    project_list = PandasModel

    encrypt_fields = TASK_FIELDS_TO_ENCRYPT
    eval_fields = TASK_FIELDS_APPLY_EVAL

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

        saved_tasks_path = path / SAVED_TASKS_FILENAME
        if saved_tasks_path.exists():
            original_df = pd.read_csv(saved_tasks_path, index_col=0)
        else:
            columns = list(TaskEntry.model_fields.keys())
            original_df = pd.DataFrame(columns=columns)

        initial_file_data = load_tasks_from_csv(path, self.encrypt_fields, self.eval_fields)

        final_df = create_updated_df(original_df, all_note_data, initial_file_data,
                                     path, self.encrypt_fields)
        final_df.to_csv(path / SAVED_TASKS_FILENAME)

        delete_old_hash_browns(final_df, path)

    def save_json_dict_into_model(self, note_data: dict):
        try:
            note_data = update_note_data(note_data)
            note_data = TaskEntry(**note_data).model_dump()

            assert (note_data['status'] in STATUS_TYPES)
            model_list = self.__getattribute__(note_data['status'])
        except Exception:
            print(f'json dict {note_data} cannot be read.')
            return

        TaskIdProvider.update_max_id(note_data['id_number'])
        add_new_item_to_model_list(model_list, note_data)

    def load_from_folder(self, rel_path: str):
        path = self.check_folder_path(rel_path)

        decrypted_note_data = load_tasks_from_csv(path, self.encrypt_fields, self.eval_fields)
        for key in sorted(decrypted_note_data.keys()):
            self.save_json_dict_into_model(decrypted_note_data[key])

        decrypted_project_data = load_projects_from_csv(path)
