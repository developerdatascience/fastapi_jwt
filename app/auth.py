from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from app.config import settings
import secrets
from sqlalchemy.orm import Session
from app.models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta:timedelta = None):
    to_encode = data.copy()
    expire = datetime.now() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def generate_reset_token() -> str:
    return secrets.token_urlsafe(32)

def set_reset_token(db: Session, user: User):
    reset_token = generate_reset_token()
    user.reset_token = reset_token
    db.commit()
    return reset_token