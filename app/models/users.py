from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    reset_token = Column(String, nullable=True)
    full_name = Column(String)
    profile_picture = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now())

    devices = relationship("HouseholdDevice", back_populates="owner")
    subscriptions = relationship("Subscription", back_populates="user")
    login_logs = relationship("UserLoginLog", back_populates="user")


class UserLoginLog(Base):
    __tablename__ = "user_login_logs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    login_time = Column(DateTime, default=datetime.now())
    logout_time = Column(DateTime)
    user = relationship("User", back_populates="login_logs")




