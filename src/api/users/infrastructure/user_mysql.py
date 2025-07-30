from sqlalchemy.orm import Session
from src.api.users.domain.user_repository import UserRepository
from src.api.users.domain.user import User
from src.db.database import Base
from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DateTime
from sqlalchemy.sql import func
from typing import Optional, List
import enum


class UserRole(enum.Enum):
    supervisor = 'supervisor'
    farmer = 'farmer'


class UserModel(Base):
    __tablename__ = 'User'
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    supervisor_id = Column(Integer, ForeignKey('User.id'), nullable=True)
    created_at = Column(DateTime, server_default=func.now())


class UserMySQLRepository(UserRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str) -> Optional[User]:
        user = self.db.query(UserModel).filter(
            UserModel.email == email).first()
        return self._to_domain(user) if user else None

    def get_by_id(self, user_id: int) -> Optional[User]:
        user = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        return self._to_domain(user) if user else None

    def create(self, user: User) -> User:
        db_user = UserModel(
            full_name=user.full_name,
            email=user.email,
            password_hash=user.password_hash,
            role=user.role,
            supervisor_id=user.supervisor_id
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return self._to_domain(db_user)

    def list_farmers_by_supervisor(self, supervisor_id: int) -> List[User]:
        farmers = self.db.query(UserModel).filter(
            UserModel.supervisor_id == supervisor_id).all()
        return [self._to_domain(f) for f in farmers]

    def _to_domain(self, user_model: UserModel) -> User:
        return User(
            id=user_model.id,
            full_name=user_model.full_name,
            email=user_model.email,
            password_hash=user_model.password_hash,
            role=user_model.role.value,
            supervisor_id=user_model.supervisor_id,
            created_at=user_model.created_at
        )
