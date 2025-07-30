from datetime import datetime
from typing import Optional


class Notification:
    def __init__(self, id: int, user_id: int, pond_id: int, message: str, type: str, is_read: bool, created_at: datetime):
        self.id = id
        self.user_id = user_id
        self.pond_id = pond_id
        self.message = message
        self.type = type  # e.g., 'alert', 'info', etc.
        self.is_read = is_read
        self.created_at = created_at
