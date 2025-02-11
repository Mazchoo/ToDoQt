''' Task control functions that change the state of the project models '''
from unittest.mock import MagicMock

from PyQt5.QtCore import QModelIndex

from Common.ClassMethod import ClassMethod
from Common.ModelViewController import QtControlFunction

from Controller.Controller import ToDoListController
from Controller.ControlHelpers import (
    update_project_table, filter_available_tasks_for_selected_project, disable_time_edits,
    delete_all_tasks_with_project_id
)

from Models.ProjectEntry import Project, create_new_project


@ClassMethod(ToDoListController)
@QtControlFunction(True)
def add_new_project(self: ToDoListController, _click: bool):
    ''' Add new project if project name is available '''
    if project_name := self.layout.newProject_lineEdit.text():
        try:
            new_project = Project(**create_new_project(project_name))
        except ValueError as e:
            print(f"New project is invalid schema with error {e}")
            return

        self.model.project_list = self.model.project_list.add_project(new_project)
        update_project_table(self.layout.project_tableView, self.model.project_list)

        self.layout.newProject_lineEdit.setText("")
        self.layout.addNewProject_pushButton.setEnabled(False)
        self.layout.backup_pushButton.setEnabled(True)


@ClassMethod(ToDoListController)
@QtControlFunction(MagicMock())
def project_row_click(self: ToDoListController, clicked_index: QModelIndex):
    ''' Reset GUI for clicking on a project '''
    prev_project_id = self.model.project_list.current_project_id
    row = clicked_index.row()
    self.model.project_list.set_selected_row(row)
    project_id = self.model.project_list.current_project_id
    self.project_description_handler.stop_editing()

    if project_id != prev_project_id:
        filter_available_tasks_for_selected_project(self.model, project_id)

        self.layout.newTask_lineEdit.setEnabled(True)
        self.layout.saveTaskChanges_pushButton.setEnabled(False)
        self.layout.deleteTask_pushButton.setEnabled(False)
        self.layout.taskDescription_textEdit.setText("")
        self.layout.taskDescription_textEdit.setEnabled(False)
        disable_time_edits(self)

        self.layout.saveProjectChanges_pushButton.setEnabled(False)

        self.layout.deleteProject_pushButton.setEnabled(True)
        self.layout.projectDescription_textEdit.setEnabled(True)
        text_descrition = self.model.project_list.current_description
        self.layout.projectDescription_textEdit.setText(text_descrition)
        self.project_description_handler.render_markdown()


@ClassMethod(ToDoListController)
@QtControlFunction(MagicMock())
def project_header_click(self: ToDoListController, _clicked_index: QModelIndex):
    ''' Remove project selection '''
    self.model.project_list.set_selected_row(None)
    filter_available_tasks_for_selected_project(self.model, None)

    self.layout.newTask_lineEdit.setText("")
    self.layout.newTask_lineEdit.setEnabled(False)
    self.layout.saveTaskChanges_pushButton.setEnabled(False)
    self.layout.deleteTask_pushButton.setEnabled(False)
    self.layout.taskDescription_textEdit.setText("")
    self.layout.taskDescription_textEdit.setEnabled(False)
    disable_time_edits(self)

    self.layout.project_tableView.clearSelection()
    self.layout.deleteProject_pushButton.setEnabled(False)
    self.layout.projectDescription_textEdit.setText("")
    self.layout.projectDescription_textEdit.setEnabled(False)


@ClassMethod(ToDoListController)
@QtControlFunction()
def enable_project_save(self: ToDoListController):
    ''' Enable project save button '''
    self.layout.backup_pushButton.setEnabled(True)


@ClassMethod(ToDoListController)
@QtControlFunction()
def check_enable_project_save(self: ToDoListController):
    ''' If project description changed, enable save project changes '''
    if self.model.project_list.selected_row is not None and self.project_description_handler.is_editing:
        old_description = self.model.project_list.current_description
        description_changed = self.layout.projectDescription_textEdit.toPlainText() != old_description
        self.layout.saveProjectChanges_pushButton.setEnabled(description_changed)


@ClassMethod(ToDoListController)
@QtControlFunction(True)
def save_project_description(self: ToDoListController, _click: bool):
    ''' Update project model with new description '''
    if self.model.project_list.selected_row is not None:
        description = self.project_description_handler.raw_markdown
        self.model.project_list.set_current_description(description)

        self.layout.saveProjectChanges_pushButton.setEnabled(False)
        self.layout.backup_pushButton.setEnabled(True)


@ClassMethod(ToDoListController)
@QtControlFunction()
def enable_add_new_project(self: ToDoListController):
    ''' If new project title not empty, enable add new task '''
    new_project_title_empty = self.layout.newProject_lineEdit.displayText() == ''
    self.layout.addNewProject_pushButton.setEnabled(not new_project_title_empty)


@ClassMethod(ToDoListController)
@QtControlFunction(True)
def delete_current_project(self: ToDoListController, _click: bool):
    ''' Delete project if selected '''
    if (project_id := self.model.project_list.current_project_id) and \
       (new_project_list := self.model.project_list.delete_selected_project()):

        self.model.project_list = new_project_list
        update_project_table(self.layout.project_tableView, self.model.project_list)

        self.layout.project_tableView.clearSelection()
        self.layout.newTask_lineEdit.setEnabled(False)
        self.layout.saveTaskChanges_pushButton.setEnabled(False)
        self.layout.deleteTask_pushButton.setEnabled(False)
        self.layout.taskDescription_textEdit.setText("")
        self.layout.taskDescription_textEdit.setEnabled(False)
        disable_time_edits(self)

        delete_all_tasks_with_project_id(self.model, project_id)

        self.layout.deleteProject_pushButton.setEnabled(False)
        self.layout.projectDescription_textEdit.setText("")
        self.layout.projectDescription_textEdit.setEnabled(False)

        self.layout.backup_pushButton.setEnabled(True)
