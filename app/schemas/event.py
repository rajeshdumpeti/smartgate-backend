from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class EventBase(BaseModel):
    student_id: Optional[int] = None
    event_type: str
    status: str
    notes: Optional[str] = None

class EventCreate(EventBase):
    pass

class EventResponse(EventBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True
