from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, EmailStr
from src.api.users.domain.user import User
from src.api.users.application.user_service import UserService
from src.api.users.infrastructure.adapters.user_Mysql import UserMysql
from src.core.db.connection import get_db
import os
from src.api.auth.application.auth_service import AuthService
from fastapi.security import HTTPBearer
import jwt
from typing import List

router = APIRouter(prefix="/api/users", tags=["users"])


def get_user_service(db: Session = Depends(get_db)):
    user_repo = UserMysql(db)
    return UserService(user_repo)


http_bearer = HTTPBearer()

# Dummy dependency for extracting user info from JWT (to be implemented)


def get_current_user(token: str = Depends(http_bearer)):
    # Decodifica el JWT y extrae el id y role reales
    secret_key = os.getenv("JWT_SECRET", "dev_secret")
    try:
        payload = jwt.decode(token.credentials, secret_key,
                             algorithms=["HS256"])
        return {"id": payload["id"], "role": payload["role"]}
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


class FarmerRequest(BaseModel):
    full_name: str
    email: EmailStr
    password: str


@router.post("/acuicultor", status_code=201)
def create_acuicultor(request: FarmerRequest, user=Depends(get_current_user), service: UserService = Depends(get_user_service)):
    if user["role"] != "supervisor":
        raise HTTPException(
            status_code=403, detail="Only supervisors can create acuicultor")
    try:
        farmer = service.create_acuicultor(
            user["id"], request.full_name, request.email, request.password)
        return {"success": True, "data": {"id": farmer.id, "full_name": farmer.full_name, "email": farmer.email}}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/me")
def get_me(user=Depends(get_current_user), service: UserService = Depends(get_user_service)):
    me = service.get_me(user["id"])
    if not me:
        raise HTTPException(status_code=404, detail="User not found")
    return {"success": True, "data": {"id": me.id, "full_name": me.full_name, "email": me.email, "role": me.role}}


@router.get("/my-acuicultor")
def acuicultor(user=Depends(get_current_user), service: UserService = Depends(get_user_service)):
    if user["role"] != "supervisor":
        raise HTTPException(
            status_code=403, detail="Only supervisors can view their acuicultor")
    acuicultor: List[User] = service.get_my_acuicultor(user["id"])
    return {"success": True, "data": [{"id": f.id, "full_name": f.full_name, "email": f.email} for f in acuicultor]}
