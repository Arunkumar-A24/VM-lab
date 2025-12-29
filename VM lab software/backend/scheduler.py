# scheduler.py

from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session
from datetime import datetime
from database import SessionLocal
from models import Booking
from config import BOOKING_STATUS


def expire_bookings():
    db: Session = SessionLocal()
    now = datetime.utcnow()

    expired = db.query(Booking).filter(
        Booking.end_time <= now,
        Booking.status != BOOKING_STATUS["EXPIRED"]
    ).all()

    for booking in expired:
        booking.status = BOOKING_STATUS["EXPIRED"]

    db.commit()
    db.close()


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(expire_bookings, "interval", seconds=30)
    scheduler.start()
