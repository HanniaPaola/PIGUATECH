from sqlalchemy import text
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthRepository:
    def __init__(self, db):
        self.db = db

    def create_user(self, full_name, email, password, role="acuicultor"):
        hashed_password = pwd_context.hash(password)

        sql = text("""
            INSERT INTO User (full_name, email, password_hash, role)
            VALUES (:full_name, :email, :password_hash, :role)
        """)
        self.db.execute(sql, {
            "full_name": full_name,
            "email": email,
            "password_hash": hashed_password,
            "role": role
        })
        self.db.commit()

    def get_user_by_email(self, email):
        sql = text("SELECT * FROM User WHERE email = :email")
        result = self.db.execute(sql, {"email": email}).fetchone()
        return dict(result._mapping) if result else None

    def verify_password(self, plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)
