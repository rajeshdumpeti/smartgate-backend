from sqlalchemy import (
    Column,
    Integer,
    String,
    JSON,
    Date,
    DateTime,
    func,
    UniqueConstraint,
)
from app.core.db import Base

class Student(Base):
    __tablename__ = "students"
    __table_args__ = (
        UniqueConstraint("name", "grade", name="uq_student_name_grade"),
    )

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String(50), unique=True, nullable=True, index=True)  # new
    name = Column(String(120), nullable=False, index=True)
    grade = Column(String(32), nullable=False, index=True)
    section = Column(String(32), nullable=True, index=True)
    date_of_birth = Column(Date, nullable=True)  # new
    parent_phone = Column(String(20), nullable=True)  # new
    photo_path = Column(String(255), nullable=True)        # local path under ./data/faces
    embedding = Column(JSON, nullable=True)                # list[float] from face_recognition
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())