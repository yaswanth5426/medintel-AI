import os
from pathlib import Path
from dotenv import load_dotenv


env_path= Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY is None:
    raise ValueError("GEMINI_API_KEY not found in .env")