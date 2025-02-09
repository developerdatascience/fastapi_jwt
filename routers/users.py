from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from models import User
from schemas import UserCreate, UserResponse, Token, ForgotPasswordRequest, ResetPasswordRequest
from auth import hash_password, verify_password, create_access_token, set_reset_token
from dependencies import get_db
from email_utils import send_reset_email
from config import settings

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = hash_password(user.password)
    new_user = User(username=user.username, email=user.email, hashed_password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login", response_model=Token)
async def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        return HTTPException(status_code=400, detail="Invalid Credentials")
    
    access_token = create_access_token(data={"sub": str(db_user.id)}, expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/forgot_password")
async def forgot_password(request: ForgotPasswordRequest, db: Session= Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=400, detail="User doest not exists")
    
    reset_token = set_reset_token(db=db, user=user)

    await send_reset_email(email=user.email, reset_token=reset_token)
    # Send `reset_token` via email (to be implemented)
    return {"message": "Reset link sent to the email", "reset_token": reset_token}


@router.post("/reset-password")
async def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.reset_token == request.token).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    
    # Verify old password
    if not verify_password(request.old_password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Old password is incorrect.")
    user.hashed_password = hash_password(request.new_password)
    user.reset_token = None
    db.commit()
    
    return {"message": "Password successfully reset"}
