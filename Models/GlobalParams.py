
LATEST_VERSION = 3
MAX_TITLE_LENGTH = 30
STATUS_TYPES = ['pending_list', 'in_progress_list', 'done_list']
LIST_VIEW_TO_STATUS_TYPE = {
    'inProgress_listView': 'in_progress_list',
    'pending_listView': 'pending_list', 
    'done_listView': 'done_list',
}

TASK_FIELDS_APPLY_EVAL = ['date_created', 'date_edited', 'date_moved', 'project_id',
                          'time_spent_seconds', 'estimated_time_seconds', 'points']
TASK_FIELDS_TO_ENCRYPT = ['title', 'description', 'project_id', 'project_id',
                          'time_spent_seconds', 'estimated_time_seconds', 'points',
                          'date_created', 'date_edited', 'date_moved']

PROJECT_FIELDS_TO_DISPLAY = {'title': "Title",
                             'last_update': "Latest",
                             'hr_remain': 'Remain',
                             'hr_spent': 'Spent',
                             'perc_complete': 'Time %',
                             'points_gained': 'points'}

SAVED_TASKS_FILENAME = 'saved_tasks.csv'
SAVED_PROJECTS_FILENAME = 'saved_projects.csv'


class TaskIdProvider:
    max_id = 0

    @staticmethod
    def get_new_id():
        TaskIdProvider.max_id += 1
        return TaskIdProvider.max_id

    @staticmethod
    def update_max_id(new_id):
        TaskIdProvider.max_id = max(new_id, TaskIdProvider.max_id)


class ProjectIdProvider:
    max_id = 0

    @staticmethod
    def get_new_id():
        ProjectIdProvider.max_id += 1
        return ProjectIdProvider.max_id

    @staticmethod
    def update_max_id(new_id):
        ProjectIdProvider.max_id = max(new_id, ProjectIdProvider.max_id)
