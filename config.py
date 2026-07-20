from pathlib import Path
from dotenv import load_dotenv
import os

BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / ".env")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

print("BASE_DIR:", BASE_DIR)
print("ENV EXISTIERT:", (BASE_DIR / ".env").exists())
print("API:", OPENAI_API_KEY)