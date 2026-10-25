import os
from pathlib import Path
from dotenv import load_dotenv

# Nạp file .env nếu có
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

GMAIL_USER = os.getenv("GMAIL_USER", "")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD", "")

POLL_INTERVAL_SECONDS = int(os.getenv("POLL_INTERVAL_SECONDS", "5"))

# Ngưỡng phát hiện Flood Attack
FLOOD_WINDOW_SECONDS = int(os.getenv("FLOOD_WINDOW_SECONDS", "60"))
FLOOD_EMAIL_THRESHOLD = int(os.getenv("FLOOD_EMAIL_THRESHOLD", "5"))
FLOOD_SIMILARITY_THRESHOLD = float(os.getenv("FLOOD_SIMILARITY_THRESHOLD", "0.75"))

# Đường dẫn lưu model & logs
MODEL_PATH = BASE_DIR / "rf_spam_model.pkl"
VECTORIZER_PATH = BASE_DIR / "tfidf_vectorizer.pkl"
DATABASE_LOG_PATH = BASE_DIR / "email_logs.json"
