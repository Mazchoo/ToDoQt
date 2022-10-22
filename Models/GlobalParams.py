
LATEST_VERSION = 2
MAX_TITLE_LENGTH = 20
STATUS_TYPES = {'pending_list', 'in_progress_list', 'done_list'}
LIST_VIEW_TO_STATUS_TYPE = {
    'inProgress_listView': 'in_progress_list',
    'pending_listView': 'pending_list', 
    'done_listView': 'done_list',
}
FIELDS_TO_EVAL = {'date_created', 'date_edited', 'date_moved'}
FIELDS_TO_ENCRYPT = {'title', 'description'}

class NoteIdProvider:
    max_id = 0
    
    @staticmethod
    def get_new_id():
        NoteIdProvider.max_id += 1
        return NoteIdProvider.max_id

    @staticmethod
    def update_max_id(new_id):
        NoteIdProvider.max_id = max(new_id, NoteIdProvider.max_id)
