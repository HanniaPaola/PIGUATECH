from datetime import datetime
from typing import Optional


class Report:
    def __init__(self, id: int, user_id: int, title: str, file_url: Optional[str], created_at: datetime):
        self.id = id
        self.user_id = user_id
        self.title = title
        self.file_url = file_url
        self.created_at = created_at
