from typing import List, Optional
from src.api.users.domain.user_repository import UserRepository
from src.api.users.domain.user import User
import bcrypt
from datetime import datetime, timezone


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def create_acuicultor(self, supervisor_id: int, full_name: str, email: str, password: str) -> User:
        if self.user_repository.get_by_email(email):
            raise ValueError('Email already exists')
        password_hash = bcrypt.hashpw(
            password.encode(), bcrypt.gensalt()).decode()
        user = User(
            id=0,  # to be set by DB
            full_name=full_name,
            email=email,
            password_hash=password_hash,
            role='acuicultor',
            supervisor_id=supervisor_id,
            created_at=datetime.now(timezone.utc)
        )
        return self.user_repository.create(user)

    def get_me(self, user_id: int) -> Optional[User]:
        return self.user_repository.get_by_id(user_id)

    def get_my_acuicultores(self, supervisor_id: int) -> List[User]:
        return self.user_repository.list_acuicultores_by_supervisor(supervisor_id)

