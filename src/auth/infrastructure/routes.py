from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.core.db.connection import get_db
from src.auth.infrastructure.repository import AuthRepository
from src.auth.application.auth_service import AuthService
from src.auth.domain.entities import UserCreate, UserLogin
from src.auth.infrastructure.security import get_current_user, verify_admin
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

bearer_scheme = HTTPBearer()


router = APIRouter(prefix="/auth", tags=["auth"])

def get_auth_service(db: Session = Depends(get_db)):
    repo = AuthRepository(db)
    return AuthService(repo)

@router.post("/register")
def register(user: UserCreate, service: AuthService = Depends(get_auth_service)):
    try:
        service.register_user(user)
        return {"msg": "User created"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
def login(user: UserLogin, service: AuthService = Depends(get_auth_service)):
    db_user = service.authenticate_user(user.email, user.password)
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = service.create_access_token({
        "sub": db_user["email"],
        "role": db_user["role"]
    })
    return {"access_token": token, "token_type": "bearer"}

@router.get("/supervisor-area")
def supervisor_area(user: dict = Depends(verify_admin)):
    return {"message": f"Hola supervisor {user['sub']}!"}

@router.get("/profile")
def profile(user: dict = Depends(get_current_user)):
    return {"user": user}
