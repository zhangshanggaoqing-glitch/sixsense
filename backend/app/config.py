import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
RAW_SOURCE_DIR = Path(os.getenv("CET6_RAW_SOURCE_DIR", "/home/stone/桌面/听力/01-六级历年真题及答案解析+听力音频"))
DATA_DIR = Path(os.getenv("SIX_SENSE_DATA_DIR", str(BASE_DIR / "data")))
DERIVED_DIR = DATA_DIR / "derived"
DB_PATH = DATA_DIR / "sixsense.db"

# Ensure directories exist
DATA_DIR.mkdir(parents=True, exist_ok=True)
DERIVED_DIR.mkdir(parents=True, exist_ok=True)
