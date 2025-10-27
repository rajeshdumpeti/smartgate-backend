from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models.student import Student
from app.schemas.student import StudentCreate, StudentOut
from app.utils.file_utils import save_base64_image
from app.utils.face_utils import generate_face_encoding

router = APIRouter()

@router.post("/register", response_model=StudentOut)
def register_student(payload: StudentCreate, db: Session = Depends(get_db)):
    """
    Register a new student with optional base64 photo.
    Saves photo, generates face embedding, and inserts record.
    """
    # 1️⃣ Save image (if provided)
    photo_path = None
    if payload.photo_base64:
        photo_path = save_base64_image(payload.photo_base64, payload.name)
        if not photo_path:
            raise HTTPException(status_code=400, detail="Failed to save photo")

    # 2️⃣ Generate embedding
    embedding = None
    if photo_path:
        embedding = generate_face_encoding(photo_path)
        if embedding is None:
            raise HTTPException(status_code=400, detail="No face detected in uploaded image")

    # 3️⃣ Create DB entry
    new_student = Student(
        name=payload.name,
        grade=payload.grade,
        section=payload.section,
        photo_path=photo_path,
        embedding=embedding,
    )
    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return new_student


@router.get("/", response_model=list[StudentOut])
def get_all_students(db: Session = Depends(get_db)):
    """Return all registered students."""
    students = db.query(Student).order_by(Student.created_at.desc()).all()
    return students
