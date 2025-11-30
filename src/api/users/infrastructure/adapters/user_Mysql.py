from src.api.users.domain.user_repository import UserRepository
from src.api.users.domain.user import User
from src.api.users.infrastructure.models import UserModel
from src.core.db.connection import get_db
from typing import Optional, List
from sqlalchemy.orm import Session
from datetime import datetime, timezone


class UserMysql(UserRepository):
    def __init__(self, db: Optional[Session] = None):
        self.db = db or next(get_db())

    def get_by_email(self, email: str) -> Optional[User]:
        user = self.db.query(UserModel).filter(
            UserModel.email == email).first()
        if user:
            return User(
                id=user.id,
                full_name=user.full_name,
                email=user.email,
                password_hash=user.password_hash,
                role=user.role,
                supervisor_id=user.supervisor_id,
                created_at=user.created_at
            )
        return None

    def get_by_id(self, user_id: int) -> Optional[User]:
        user = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        if user:
            return User(
                id=user.id,
                full_name=user.full_name,
                email=user.email,
                password_hash=user.password_hash,
                role=user.role,
                supervisor_id=user.supervisor_id,
                created_at=user.created_at
            )
        return None

    def create(self, user: User) -> User:
        db_user = UserModel(
            full_name=user.full_name,
            email=user.email,
            password_hash=user.password_hash,
            role=user.role,
            supervisor_id=user.supervisor_id,
            created_at=user.created_at
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        user.id = db_user.id
        return user

    def list_acuicultores_by_supervisor(self, supervisor_id: int) -> List[User]:
        acuicultor = self.db.query(UserModel).filter(
            UserModel.supervisor_id == supervisor_id, UserModel.role == 'acuicultor').all()
        return [User(
            id=u.id,
            full_name=u.full_name,
            email=u.email,
            password_hash=u.password_hash,
            role=u.role,
            supervisor_id=u.supervisor_id,
            created_at=u.created_at
        ) for u in acuicultor]
