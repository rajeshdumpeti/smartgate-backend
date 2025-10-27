from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

# ---- Base Schema ----
class StudentBase(BaseModel):
    name: str = Field(..., example="Aarav Reddy")
    grade: str = Field(..., example="5th")
    section: Optional[str] = Field(None, example="A")

# ---- Create Schema (Incoming Request) ----
class StudentCreate(StudentBase):
    photo_base64: Optional[str] = Field(
        None,
        description="Base64-encoded face image sent from frontend during registration",
    )

# ---- Output Schema (Response) ----
class StudentOut(StudentBase):
    id: int
    photo_path: Optional[str]
    embedding: Optional[List[float]]
    created_at: datetime

    class Config:
        orm_mode = True  # allows returning SQLAlchemy objects directly
