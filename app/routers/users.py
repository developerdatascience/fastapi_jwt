from fastapi import Depends, HTTPException, status, APIRouter, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import timedelta
from app.models import User
from app.schemas import UserCreate, UserResponse, Token, ForgotPasswordRequest, ResetPasswordRequest
from app.auth import hash_password, verify_password, create_access_token, set_reset_token
from app.dependencies import get_db
from app.email_utils import send_reset_email
from app.config import settings
import logging

router = APIRouter(prefix="/users", tags=["Users"])

# Set up template rendering
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("root.html", {"request": request})

@router.post("/register", response_class=HTMLResponse)
async def register(request: Request, 
                   username: str = Form(...),
                   email: str = Form(...),
                   password: str = Form(...),
                   db: Session = Depends(get_db)):
    try:
        if db.query(User).filter(User.email == email).first():
            raise HTTPException(status_code=400, detail="Email already registered")

        hashed_pw = hash_password(password)
        new_user = User(username=username, email=email, hashed_password=hashed_pw)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return templates.TemplateResponse("registration.html", {"request": request, "message": "User registered successfully"})
    except HTTPException as e:
        logging.error(f"HTTP error occurred: {e.detail}")
        raise e
    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": "Internal Server Error"})

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
