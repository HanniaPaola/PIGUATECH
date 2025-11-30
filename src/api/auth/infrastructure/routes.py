from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, EmailStr

from src.api.auth.application.auth_service import AuthService
# Asegúrate de que existe
from src.api.auth.infrastructure.adapters.user_Mysql import UserMysql
from src.core.db.connection import get_db
from sqlalchemy.orm import Session
import os


router = APIRouter(prefix="/api/auth", tags=["auth"])


def get_auth_service(db: Session = Depends(get_db)):
    user_repo = UserMysql(db)
    secret_key = os.getenv("JWT_SECRET", "dev_secret")
    algorithm = "HS256"
    return AuthService(user_repo, secret_key, algorithm)


class RegisterRequest(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    role: str 



class LoginRequest(BaseModel):
    email: EmailStr
    password: str


@router.post("/register", status_code=201)
def register(request: RegisterRequest, service: AuthService = Depends(get_auth_service)):
    try:
        user = service.register_user(
            request.full_name,
            request.email,
            request.password,
            request.role,
            None  # supervisor_id (si luego lo quieres asignar)
        )
        return {
            "success": True,
            "data": {
                "id": user.id,
                "full_name": user.full_name,
                "email": user.email,
                "role": user.role
            }
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@router.post("/login")
def login(request: LoginRequest, service: AuthService = Depends(get_auth_service)):
    result = service.login(request.email, request.password)
    if not result:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token, user = result

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "role": user.role,
            "email": user.email,
            "full_name": user.full_name
        }
    }
