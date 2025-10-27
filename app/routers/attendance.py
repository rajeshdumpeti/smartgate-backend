from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.utils.face_utils import match_face_to_student
from app.utils.file_utils import save_base64_image
from app.models.event import Event
from pydantic import BaseModel

router = APIRouter()

class FaceDetectRequest(BaseModel):
    image_base64: str
    event_type: str = "entry"

@router.post("/detect")
def detect_face(payload: FaceDetectRequest, db: Session = Depends(get_db)):
    image_base64 = payload.image_base64
    event_type = payload.event_type
    """
    Detect a student from the given image and log attendance.
    event_type: "entry" or "exit"
    """
    # 1️⃣ Save incoming image to /data/faces/detections
    photo_path = save_base64_image(image_base64, f"detect_{event_type}")
    if not photo_path:
        raise HTTPException(status_code=400, detail="Failed to save detection image")

    # 2️⃣ Match face with database
    matched_student, distance = match_face_to_student(db, photo_path)

    # 3️⃣ Log event
    if matched_student:
        event = Event(
            student_id=matched_student.id,
            event_type=event_type,
            status="success",
            notes=f"Matched: {matched_student.name} (distance={distance:.2f})",
        )
        db.add(event)
        db.commit()
        db.refresh(event)
        return {
            "status": "success",
            "message": f"Match found: {matched_student.name}",
            "student_id": matched_student.id,
            "distance": distance,
            "event_type": event_type,
            "timestamp": event.timestamp,
        }
    else:
        event = Event(
            student_id=None,
            event_type=event_type,
            status="unknown",
            notes=f"No match (min_distance={distance})",
        )
        db.add(event)
        db.commit()
        return {
            "status": "unknown",
            "message": "No match found",
            "distance": distance,
            "event_type": event_type,
        }
