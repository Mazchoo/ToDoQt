
LATEST_VERSION = 3
MAX_TITLE_LENGTH = 30
MAX_PROJECT_TITLE_LENGTH = 10
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
