from typing import Optional
from src.api.auth.domain.user_repository import UserRepository
from src.api.auth.domain.user import User
import bcrypt
import jwt
from datetime import datetime, timedelta, timezone


class AuthService:
    def __init__(self, user_repository: UserRepository, secret_key: str, algorithm: str):
        self.user_repository = user_repository
        self.secret_key = secret_key
        self.algorithm = algorithm

    def register_user(self, full_name: str, email: str, password: str, role: str, supervisor_id: Optional[int]):
        if self.user_repository.get_by_email(email):
            raise ValueError("El correo ya está registrado, intenta con otro")

        password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        user = User(
            id=0,
            full_name=full_name,
            email=email,
            password_hash=password_hash,
            role=role,
            supervisor_id=supervisor_id,
            created_at=datetime.now(timezone.utc)
        )

        return self.user_repository.create(user)

    def login(self, email: str, password: str) -> Optional[str]:
        user = self.user_repository.get_by_email(email)
        if not user or not bcrypt.checkpw(password.encode(), user.password_hash.encode()):
            return None
        payload = {
            'id': user.id,
            'role': user.role,
            'exp': datetime.now(timezone.utc) + timedelta(hours=24)
        }
        token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        return token, user
