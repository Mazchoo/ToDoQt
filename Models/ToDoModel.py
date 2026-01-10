"""Storage class for all model data of app, loading and saving ect"""

from typing import Dict, List, Optional

from PyQt5.QtGui import QStandardItemModel

from Common.QtModel import QtStaticModel

from Models.ProjectProxyFilter import ProjectFilterProxyModel

from Models.ModelParameters import (
    TASK_FIELDS_APPLY_EVAL,
    TASK_FIELDS_TO_ENCRYPT,
    PROJECT_FIELDS_APPLY_EVAL,
    PROJECT_FIELDS_TO_ENCRYPT,
    STATUS_TYPES,
    SAVED_TASKS_FILENAME,
    SAVED_PROJECTS_FILENAME,
)
from Models.TaskEntry import TaskEntry, update_task_data, TASK_ID_PROVIDER
from Models.ProjectEntry import Project, PROJECT_ID_PROVIDER
from Models.FileHelpers import (
    delete_old_hash_browns,
    get_hash_file_from_task_data,
    get_hash_file_from_project_data,
    convert_list_to_task_data,
    load_content_from_csv,
    add_new_item_to_model_list,
    save_model_data,
    check_folder_path,
)
from Models.ProjectTable import ProjectTableModel


class ToDoModel(QtStaticModel):
    """Singleton that stores Qt Model information"""

    pending_list = QStandardItemModel
    pending_filter = ProjectFilterProxyModel
    in_progress_list = QStandardItemModel
    in_progress_filter = ProjectFilterProxyModel
    done_list = QStandardItemModel
    done_filter = ProjectFilterProxyModel
    project_list = ProjectTableModel

    def get_all_task_data(self) -> Dict[str, List[dict]]:
        """Get all task data as lists from models in a serializable form"""
        all_task_data = []
        for status in STATUS_TYPES:
            model_list = self.get_model_from_status(status)
            if model_list is not None:
                all_task_data.extend(convert_list_to_task_data(model_list))

        return {get_hash_file_from_task_data(task): task for task in all_task_data}

    def get_all_project_data(self) -> Dict[str, List[dict]]:
        """Get all project data is serializable form"""
        all_project_data = self.project_list.save_dump
        return {
            get_hash_file_from_project_data(project): project
            for project in all_project_data
        }

    def save_to_folder(self, rel_path: str):
        """Save all models to encrypted csv"""
        path = check_folder_path(rel_path)

        task_save_path = path / SAVED_TASKS_FILENAME
        all_task_data = self.get_all_task_data()
        original_task_data = load_content_from_csv(
            task_save_path, TASK_FIELDS_TO_ENCRYPT, TASK_FIELDS_APPLY_EVAL
        )

        task_save_df = save_model_data(
            task_save_path,
            list(TaskEntry.model_fields.keys()),
            TASK_FIELDS_TO_ENCRYPT,
            all_task_data,
            original_task_data,
        )

        project_save_path = path / SAVED_PROJECTS_FILENAME
        all_project_data = self.get_all_project_data()
        original_project_data = load_content_from_csv(
            project_save_path, PROJECT_FIELDS_TO_ENCRYPT, PROJECT_FIELDS_APPLY_EVAL
        )

        project_save_df = save_model_data(
            project_save_path,
            list(Project.model_fields.keys()),
            PROJECT_FIELDS_TO_ENCRYPT,
            all_project_data,
            original_project_data,
        )

        delete_old_hash_browns(task_save_df.index.append(project_save_df.index), path)

    def get_model_from_status(self, status: str) -> Optional[QStandardItemModel]:
        """Get model corresponding to status"""
        if status == "pending_list":
            return self.pending_list
        if status == "in_progress_list":
            return self.in_progress_list
        if status == "done_list":
            return self.done_list
        return None

    def load_task_json_dict_into_model(self, task_data: dict):
        """Load (and check) decrypted task into corresponding model list"""
        try:
            task_data = update_task_data(task_data)
            task_data = TaskEntry(**task_data).model_dump()
            model_list = self.get_model_from_status(task_data["status"])
            if model_list is None:
                raise ValueError(f"Cannot parse task status {task_data['status']}")
        except ValueError as e:
            print(f"json dict {task_data} cannot be read {e}")
            return

        TASK_ID_PROVIDER.update_max_id(task_data["id_number"])
        add_new_item_to_model_list(model_list, task_data)

    def load_project_json_dict_into_model(
        self, project_data: dict
    ) -> Optional[Project]:
        """Parse decrypted project data into a pydantic model"""
        try:
            project = Project(**project_data)
        except ValueError as e:
            print(f"json dict {project_data} cannot be read {e}")
            return None
        PROJECT_ID_PROVIDER.update_max_id(project_data["id_number"])
        return project

    def load_from_folder(self, rel_path: str):
        """Load model contents from a folder of encrypted csv's and stored keys"""
        path = check_folder_path(rel_path)

        decrypted_note_data = load_content_from_csv(
            path / SAVED_TASKS_FILENAME, TASK_FIELDS_TO_ENCRYPT, TASK_FIELDS_APPLY_EVAL
        )
        for data in decrypted_note_data.values():
            self.load_task_json_dict_into_model(data)

        self.pending_filter = ProjectFilterProxyModel(self.pending_list)
        self.in_progress_filter = ProjectFilterProxyModel(self.in_progress_list)
        self.done_filter = ProjectFilterProxyModel(self.done_list)

        decrypted_project_data = load_content_from_csv(
            path / SAVED_PROJECTS_FILENAME,
            PROJECT_FIELDS_TO_ENCRYPT,
            PROJECT_FIELDS_APPLY_EVAL,
        )
        all_projects = []
        for data in decrypted_project_data.values():
            if project := self.load_project_json_dict_into_model(data):
                all_projects.append(project)
        all_projects.sort(key=lambda x: x.last_update, reverse=True)

        self.project_list = ProjectTableModel(all_projects)
