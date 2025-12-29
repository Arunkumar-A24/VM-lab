# schemas.py

from pydantic import BaseModel
from datetime import datetime

class BookingCreate(BaseModel):
    user_name: str
    zone: str
    start_time: datetime
    end_time: datetime

class BookingResponse(BaseModel):
    id: int
    user_name: str
    zone: str
    start_time: datetime
    end_time: datetime
    status: str

    class Config:
        orm_mode = True
