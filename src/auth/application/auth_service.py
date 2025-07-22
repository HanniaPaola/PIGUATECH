from datetime import datetime, timedelta
from jose import jwt

SECRET_KEY = "PIGUATECH_1.0.0"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

class AuthService:
    def __init__(self, repo):
        self.repo = repo

    def register_user(self, user_data):
        if user_data.password != user_data.confirm_password:
            raise ValueError("Passwords do not match")

        if self.repo.get_user_by_email(user_data.email):
            raise ValueError("Email already registered")

        self.repo.create_user(
            full_name=user_data.full_name,
            email=user_data.email,
            password=user_data.password,
            role=user_data.role
        )

    def authenticate_user(self, email, password):
        user = self.repo.get_user_by_email(email)
        if not user:
            return None
        if not self.repo.verify_password(password, user["password_hash"]):
            return None
        return user

    def create_access_token(self, data: dict, expires_delta: timedelta = None):
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
