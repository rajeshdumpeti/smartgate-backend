import cv2
import base64
import requests
import numpy as np
from pathlib import Path

# Backend detection API endpoint
API_URL = "http://127.0.0.1:8000/api/v1/attendance/detect"

# Directory to temporarily save frames
TEMP_DIR = Path("data/live_frames")
TEMP_DIR.mkdir(parents=True, exist_ok=True)

def encode_frame_to_base64(frame):
    """Convert OpenCV frame to base64 string."""
    _, buffer = cv2.imencode(".jpg", frame)
    jpg_as_text = base64.b64encode(buffer).decode("utf-8")
    return f"data:image/jpeg;base64,{jpg_as_text}"

def send_frame_to_backend(base64_str, event_type="entry"):
    """Send current frame to FastAPI for detection."""
    try:
        response = requests.post(
            API_URL,
            json={"image_base64": base64_str, "event_type": event_type},
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            status = data.get("status")
            msg = data.get("message", "")
            print(f"[API] {status.upper()} - {msg}")
        else:
            print(f"[API ERROR] {response.status_code} {response.text}")
    except Exception as e:
        print(f"[ERROR] Could not send frame: {e}")

def start_camera():
    print("🎥 Starting SmartGate Live Camera...")
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("❌ Camera not found or permission denied.")
        return

    frame_counter = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Show camera feed
        cv2.imshow("SmartGate - Press [Q] to Quit", frame)

        # Process every 30th frame (adjust as needed)
        frame_counter += 1
        if frame_counter % 30 == 0:
            print("[DEBUG] Capturing frame for face match...")
            base64_str = encode_frame_to_base64(frame)
            send_frame_to_backend(base64_str, event_type="entry")

        # Exit loop on Q key
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("🛑 SmartGate Camera stopped.")

if __name__ == "__main__":
    start_camera()
