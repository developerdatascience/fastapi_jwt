from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.config import settings
from app.models import User

def get_db():
    db: Session = SessionLocal()
    try:
        yield db  # Ensure it properly yields the database session
    except Exception as e:
        print(f"Database error: {e}")  # Debugging
    finally:
        db.close()


def get_current_user(token: str= Depends(lambda: None), db: Session= Depends(get_db)):
    credential_exception = HTTPException(
        status_code= status.HTTP_401_UNAUTHORIZED,
        detail="Invalid Credentials",
        headers= {"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms= [settings.ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credential_exception
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise credential_exception
        return user
    except JWTError:
        raise credential_exception