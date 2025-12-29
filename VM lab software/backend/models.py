# models.py

from sqlalchemy import Column, Integer, String, DateTime
from database import Base

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, nullable=False)
    zone = Column(String, nullable=False)   # Red / Yellow / Green
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    status = Column(String, nullable=False)
