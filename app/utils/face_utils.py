import face_recognition
import numpy as np
from typing import List, Optional
from pathlib import Path
from sqlalchemy.orm import Session
from app.models.student import Student


def generate_face_encoding(image_path: str) -> Optional[List[float]]:
    """
    Given an image path, detect face and return 128-d embedding as list.
    Returns None if no face found.
    """
    try:
        image = face_recognition.load_image_file(image_path)
        encodings = face_recognition.face_encodings(image)

        if len(encodings) == 0:
            print(f"[face_utils] No face found in {image_path}")
            return None

        return encodings[0].tolist()
    except Exception as e:
        print(f"[face_utils] Error generating encoding: {e}")
        return None


def match_face_to_student(db: Session, image_path: str, tolerance: float = 0.6):
    """
    Compare the given image to all known student embeddings.
    Returns (Student, distance) if match found, else (None, None).
    """
    try:
        unknown_encoding = generate_face_encoding(image_path)
        if unknown_encoding is None:
            print("[face_utils] No face detected in the uploaded image.")
            return None, None

        # pull students that have an embedding
        students = db.query(Student).filter(Student.embedding.isnot(None)).all()
        print(f"[DEBUG] Loaded {len(students)} students from DB")

        known_encodings = []
        valid_students = []
        for s in students:
            if not s.embedding:  # Add check for empty embedding
                continue
            emb = np.array(s.embedding, dtype=float)
            if emb.ndim > 1:
                emb = emb.flatten()
            if emb.shape[0] == 128:
                known_encodings.append(emb)
                valid_students.append(s)

        if not known_encodings:
            print("[face_utils] No valid embeddings found for comparison.")
            return None, None

        # Check if valid_students list is empty
        if not valid_students:
            print("[face_utils] No valid students found for comparison.")
            return None, None

        unknown_encoding = np.array(unknown_encoding, dtype=float).flatten()
        distances = face_recognition.face_distance(np.stack(known_encodings), unknown_encoding)

        if len(distances) == 0:
            print("[face_utils] No distances computed (empty array).")
            return None, None

        min_distance = float(np.min(distances))
        best_match_idx = int(np.argmin(distances))

        if min_distance <= tolerance:
            matched_student = valid_students[best_match_idx]
            print(f"[face_utils] Match found: {matched_student.name} (distance={min_distance:.2f})")
            return matched_student, min_distance
        else:
            print(f"[face_utils] No match within tolerance ({tolerance}). Closest={min_distance:.2f}")
            return None, min_distance

    except Exception as e:
        print(f"[face_utils] Error during face matching: {e}")
        return None, None