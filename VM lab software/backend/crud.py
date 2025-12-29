# crud.py

from sqlalchemy.orm import Session
from datetime import datetime
from models import Booking
from config import BOOKING_STATUS


def is_overlap(db: Session, zone: str, start_time: datetime, end_time: datetime):
    """
    Check overlapping bookings ONLY in the SAME zone
    """
    return db.query(Booking).filter(
        Booking.zone == zone,
        Booking.status != BOOKING_STATUS["EXPIRED"],
        Booking.start_time < end_time,
        Booking.end_time > start_time
    ).first()


def create_booking(db: Session, user_name: str, zone: str, start_time: datetime, end_time: datetime):
    # Rule 1: start must be before end
    if start_time >= end_time:
        raise ValueError("Start time must be before end time")

    # Rule 2: no past booking
    if start_time < datetime.utcnow():
        raise ValueError("Cannot book slot in the past")

    # Rule 3: overlap check (SAME ZONE ONLY)
    conflict = is_overlap(db, zone, start_time, end_time)
    if conflict:
        raise ValueError("Zone already booked for this time slot")

    booking = Booking(
        user_name=user_name,
        zone=zone,
        start_time=start_time,
        end_time=end_time,
        status=BOOKING_STATUS["SCHEDULED"]
    )

    db.add(booking)
    db.commit()
    db.refresh(booking)

    return booking

# crud.py (add below existing functions)

def check_availability(db: Session, zone: str, start_time: datetime, end_time: datetime):
    conflict = db.query(Booking).filter(
        Booking.zone == zone,
        Booking.status != BOOKING_STATUS["EXPIRED"],
        Booking.start_time < end_time,
        Booking.end_time > start_time
    ).first()

    return conflict is None

