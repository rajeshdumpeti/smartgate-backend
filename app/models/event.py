from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.core.db import Base

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=True)
    event_type = Column(String(20), nullable=False)        # "entry" or "exit"
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String(20), default="success")         # success / unknown / failed
    notes = Column(String(255), nullable=True)

    student = relationship("Student", backref="events")
