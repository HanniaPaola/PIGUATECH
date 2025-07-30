from datetime import datetime
from typing import Optional


class User:
    def __init__(self, id: int, full_name: str, email: str, password_hash: str, role: str, supervisor_id: Optional[int], created_at: datetime):
        self.id = id
        self.full_name = full_name
        self.email = email
        self.password_hash = password_hash
        self.role = role  # 'supervisor' or 'farmer'
        self.supervisor_id = supervisor_id
        self.created_at = created_at
