import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-only-secret-key")
    VISITORS_EXCEL = BASE_DIR / "visitors.xlsx"
    INVENTORY_EXCEL = BASE_DIR / "inventory.xlsx"

    DEFAULT_TOTAL_GADDA = int(os.getenv("DEFAULT_TOTAL_GADDA", "50"))
    DEFAULT_TOTAL_RAJAI = int(os.getenv("DEFAULT_TOTAL_RAJAI", "50"))
    DEFAULT_DEPOSIT_PER_ITEM = int(os.getenv("DEFAULT_DEPOSIT_PER_ITEM", "50"))

    SMS_ENABLED = os.getenv("SMS_ENABLED", "false").lower() == "true"
    FAST2SMS_API_KEY = os.getenv("FAST2SMS_API_KEY", "")
    FAST2SMS_SENDER_ID = os.getenv("FAST2SMS_SENDER_ID", "SHKREG")
