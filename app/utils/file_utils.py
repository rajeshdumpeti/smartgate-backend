import os
import base64
from datetime import datetime
from pathlib import Path
from typing import Optional

# Directory where all student photos will be saved
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "faces"
DATA_DIR.mkdir(parents=True, exist_ok=True)

def save_base64_image(base64_string: str, student_name: str) -> Optional[str]:
    """
    Save a base64 encoded image to local /data/faces directory.
    Returns the relative file path if successful.
    """
    try:
        if not base64_string:
            return None

        # Remove header if present (data:image/jpeg;base64,...)
        if "," in base64_string:
            base64_string = base64_string.split(",")[1]

        img_data = base64.b64decode(base64_string)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = student_name.replace(" ", "_").lower()
        filename = f"{safe_name}_{timestamp}.jpg"
        file_path = DATA_DIR / filename

        with open(file_path, "wb") as f:
            f.write(img_data)

        return str(file_path)
    except Exception as e:
        print(f"[file_utils] Error saving image: {e}")
        return None
