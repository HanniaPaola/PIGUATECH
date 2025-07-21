from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    confirm_password: str
    role: str 

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class User(BaseModel):
    user_id: int
    full_name: str
    email: EmailStr
    role: str

    class Config:
        from_attributes = True
