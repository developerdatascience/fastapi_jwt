from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class HouseholdDevice(Base):
    __tablename__ = "household_devices"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    purchase_date = Column(DateTime)
    last_service_date = Column(DateTime)
    days_for_next_service = Column(Integer)
    next_service_date = Column(DateTime)
    last_service_cost = Column(Float)
    user_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="devices")