import cv2
import base64
import requests
import threading
import time

API_URL = "http://127.0.0.1:8000/api/v1/attendance/detect"

is_running = False  # Global flag for camera loop

def encode_frame_to_base64(frame):
    """Convert OpenCV frame to base64 string."""
    _, buffer = cv2.imencode(".jpg", frame)
    jpg_as_text = base64.b64encode(buffer).decode("utf-8")
    return f"data:image/jpeg;base64,{jpg_as_text}"

def send_frame_to_backend(base64_str, event_type="entry"):
    """Send current frame to FastAPI detection API."""
    try:
        response = requests.post(API_URL, json={
            "image_base64": base64_str,
            "event_type": event_type
        }, timeout=10)

        if response.status_code == 200:
            data = response.json()
            print(f"[DETECT] {data.get('message', 'No message')}")
        else:
            print(f"[ERROR] {response.status_code}: {response.text}")

    except Exception as e:
        print(f"[ERROR] Could not send frame: {e}")

def camera_loop():
    """Main camera loop for continuous detection."""
    global is_running
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Camera not found or permission denied.")
        is_running = False
        return

    print("🎥 SmartGate Live Camera started. Press 'Q' in window to quit.")

    frame_counter = 0
    while is_running:
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow("SmartGate Live Feed", frame)
        frame_counter += 1

        # Process every 30th frame
        if frame_counter % 30 == 0:
            base64_str = encode_frame_to_base64(frame)
            send_frame_to_backend(base64_str)

        # Press Q to stop manually
        if cv2.waitKey(1) & 0xFF == ord("q"):
            is_running = False

    cap.release()
    cv2.destroyAllWindows()
    print("🛑 SmartGate Camera stopped.")

def start_live_detection():
    """Start the camera in a separate thread."""
    global is_running
    if is_running:
        print("⚠️ Camera already running.")
        return {"status": "running", "message": "Camera already active"}

    is_running = True
    thread = threading.Thread(target=camera_loop, daemon=True)
    thread.start()
    return {"status": "started", "message": "Live detection started"}

def stop_live_detection():
    """Stop live detection loop."""
    global is_running
    is_running = False
    return {"status": "stopped", "message": "Camera stopped"}

if __name__ == "__main__":
    is_running = True
    camera_loop()
