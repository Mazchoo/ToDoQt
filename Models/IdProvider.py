"""Class that creates instances to provide unique integer ids"""


class IdProvider:
    """Static class to update and get the latest task id"""

    def __init__(self):
        self.max_id = 0

    def get_new_id(self):
        """Generate new task id"""
        self.max_id += 1
        return self.max_id

    def update_max_id(self, new_id: int):
        """Update id for new id that is being read"""
        self.max_id = max(new_id, self.max_id)
