from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.db import engine
from app.models import student as student_model, event as event_model
from app.routers import student, attendance, event

app = FastAPI(title="SmartGate Backend", version="1.0")

# CORS for local frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(student.router, prefix="/api/v1/students", tags=["Students"])
app.include_router(event.router, prefix="/api/v1/events", tags=["Events"])
app.include_router(attendance.router, prefix="/api/v1/attendance", tags=["Attendance"])



@app.get("/")
def root():
    return {"message": "SmartGate Backend running successfully 🚀"}



@app.get("/db-check")
def check_db():
    try:
        with engine.connect() as conn:
            return {"status": "✅ Database connected successfully!"}
    except Exception as e:
        return {"error": str(e)}
