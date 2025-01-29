
import os
from pathlib import Path

from PyQt5.QtGui import QStandardItemModel

from Common.QtModel import QtStaticModel
from Models.ProjectProxyFilter import ProjectFilterProxyModel

from Models.ModelParameters import (TASK_FIELDS_APPLY_EVAL, TASK_FIELDS_TO_ENCRYPT,
                                    PROJECT_FIELDS_APPLY_EVAL, PROJECT_FIELDS_TO_ENCRYPT,
                                    STATUS_TYPES, SAVED_TASKS_FILENAME, SAVED_PROJECTS_FILENAME)
from Models.TaskEntry import TaskEntry, update_task_data, TaskIdProvider
from Models.ProjectEntry import Project, ProjectIdProvider
from Models.FileHelpers import (
    delete_old_hash_browns, get_hash_file_from_task_data, get_hash_file_from_project_data,
    convert_list_to_task_data, load_content_from_csv, add_new_item_to_model_list,
    save_data_frame
)
from Models.ProjectTable import ProjectTableModel

CWD = os.getcwd()


class ToDoModel(QtStaticModel):
    pending_list = QStandardItemModel
    pending_filter = ProjectFilterProxyModel
    in_progress_list = QStandardItemModel
    in_progress_filter = ProjectFilterProxyModel
    done_list = QStandardItemModel
    done_filter = ProjectFilterProxyModel
    project_list = ProjectTableModel

    encrypt_task_fields = TASK_FIELDS_TO_ENCRYPT
    eval_task_fields = TASK_FIELDS_APPLY_EVAL

    encrypt_project_fields = PROJECT_FIELDS_TO_ENCRYPT
    eval_project_fields = PROJECT_FIELDS_APPLY_EVAL

    def check_folder_path(self, rel_path: str):
        path = Path(f"{CWD}/{rel_path}")
        if not path.exists() or not path.is_dir():
            raise FileNotFoundError(f"Invalid directory {path}")
        return path

    def get_all_task_data(self):
        all_task_data = []
        for status in STATUS_TYPES:
            model_list = self.__getattribute__(status)
            all_task_data.extend(convert_list_to_task_data(model_list))

        return {get_hash_file_from_task_data(task): task for task in all_task_data}

    def get_all_project_data(self):
        all_project_data = self.project_list.save_dump
        return {get_hash_file_from_project_data(project): project for project in all_project_data}

    def save_to_folder(self, rel_path: str):
        path = self.check_folder_path(rel_path)

        task_save_path = path / SAVED_TASKS_FILENAME
        all_task_data = self.get_all_task_data()
        original_task_data = load_content_from_csv(task_save_path,
                                                   self.encrypt_task_fields,
                                                   self.eval_task_fields)

        task_save_df = save_data_frame(task_save_path, list(TaskEntry.model_fields.keys()),
                                       self.encrypt_task_fields, all_task_data, original_task_data)

        project_save_path = path / SAVED_PROJECTS_FILENAME
        all_project_data = self.get_all_project_data()
        original_project_data = load_content_from_csv(project_save_path,
                                                      self.encrypt_project_fields,
                                                      self.eval_project_fields)

        project_save_df = save_data_frame(project_save_path, list(Project.model_fields.keys()),
                                          self.encrypt_project_fields, all_project_data, original_project_data)

        delete_old_hash_browns(task_save_df.index.append(project_save_df.index), path)

    def load_task_json_dict_into_model(self, task_data: dict):
        try:
            task_data = update_task_data(task_data)
            task_data = TaskEntry(**task_data).model_dump()
            model_list = self.__getattribute__(task_data['status'])  # ToDo - use validation exception
        except Exception:
            print(f'json dict {task_data} cannot be read.')
        else:
            TaskIdProvider.update_max_id(task_data['id_number'])
            add_new_item_to_model_list(model_list, task_data)

    def load_project_json_dict_into_model(self, project_data: dict):
        try:
            project = Project(**project_data)
        except Exception:
            print(f'json dict {project_data} cannot be read.')
            return None
        else:
            ProjectIdProvider.update_max_id(project_data['id_number'])
            return project

    def load_from_folder(self, rel_path: str):
        path = self.check_folder_path(rel_path)

        decrypted_note_data = load_content_from_csv(path / SAVED_TASKS_FILENAME,
                                                    self.encrypt_task_fields, self.eval_task_fields)
        for data in decrypted_note_data.values():
            self.load_task_json_dict_into_model(data)

        self.pending_filter = ProjectFilterProxyModel(self.pending_list)
        self.in_progress_filter = ProjectFilterProxyModel(self.in_progress_list)
        self.done_filter = ProjectFilterProxyModel(self.done_list)

        decrypted_project_data = load_content_from_csv(path / SAVED_PROJECTS_FILENAME,
                                                       self.encrypt_project_fields, self.eval_project_fields)
        all_projects = []
        for data in decrypted_project_data.values():
            if project := self.load_project_json_dict_into_model(data):
                all_projects.append(project)
        all_projects.sort(key=lambda x: x.date_created, reverse=True)

        self.project_list = ProjectTableModel(all_projects)
