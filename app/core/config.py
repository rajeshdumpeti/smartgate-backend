from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseModel):
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    APP_ENV: str = os.getenv("APP_ENV", "development")

settings = Settings()
