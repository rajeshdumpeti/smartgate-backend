from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.core.db import get_db
from app.models.event import Event
from app.schemas.event import EventResponse

router = APIRouter()

@router.get("/", response_model=List[EventResponse])
def get_all_events(db: Session = Depends(get_db)):
    """Get all attendance events."""
    events = db.query(Event).order_by(Event.timestamp.desc()).all()
    return events


@router.get("/student/{student_id}", response_model=List[EventResponse])
def get_student_events(student_id: int, db: Session = Depends(get_db)):
    """Get events for a specific student."""
    events = (
        db.query(Event)
        .filter(Event.student_id == student_id)
        .order_by(Event.timestamp.desc())
        .all()
    )
    return events
