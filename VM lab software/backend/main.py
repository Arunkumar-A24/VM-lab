# main.py

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import Base, engine, SessionLocal
from schemas import BookingCreate, BookingResponse
from crud import create_booking, check_availability
from scheduler import start_scheduler
from models import Booking

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Zone Slot Booking Backend")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.on_event("startup")
def startup_event():
    start_scheduler()


@app.post("/book", response_model=BookingResponse)
def book_slot(data: BookingCreate, db: Session = Depends(get_db)):
    try:
        booking = create_booking(
            db=db,
            user_name=data.user_name,
            zone=data.zone,
            start_time=data.start_time,
            end_time=data.end_time
        )
        return booking
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/bookings")
def list_bookings(db: Session = Depends(get_db)):
    return db.query(Booking).all()

@app.get("/availability")
def check_zone_availability(
    zone: str,
    start_time: str,
    end_time: str,
    db: Session = Depends(get_db)
):
    from datetime import datetime

    start = datetime.fromisoformat(start_time)
    end = datetime.fromisoformat(end_time)

    available = check_availability(db, zone, start, end)

    return {
        "zone": zone,
        "available": available
    }

