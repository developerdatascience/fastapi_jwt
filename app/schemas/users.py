from pydantic import BaseModel, EmailStr
from datetime import datetime



class UserBase(BaseModel):
    email: EmailStr
    full_name: str

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    profile_picture: str | None = None

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    profile_picture: str | None = None

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    token: str
    old_password: str
    new_password: str



