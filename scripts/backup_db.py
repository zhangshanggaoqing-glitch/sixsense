#!/usr/bin/env python3
"""
SixSense SQLite Online Atomic Backup Script
- Uses SQLite online backup API to take a non-blocking snapshot even while users are practicing.
- Compresses with gzip.
- Retains backups for 30 days.
"""

import os
import sys
import time
import gzip
import shutil
import sqlite3
from datetime import datetime, timezone, timedelta
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "sixsense.db"
BACKUP_DIR = Path(os.getenv("BACKUP_DIR", "/home/ubuntu/backups/db"))
RETENTION_DAYS = 30

def perform_backup():
    if not DB_PATH.exists():
        print(f"[ERROR] Database file not found at {DB_PATH}")
        sys.exit(1)

    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    cst = timezone(timedelta(hours=8))
    timestamp_str = datetime.now(cst).strftime("%Y%m%d_%H%M%S")
    temp_target_file = BACKUP_DIR / f"sixsense_{timestamp_str}.db"
    final_gzip_file = BACKUP_DIR / f"sixsense_{timestamp_str}.db.gz"

    print(f"[{datetime.now(cst)}] Starting online atomic backup of {DB_PATH}...")
    start_time = time.time()

    # 1. Atomic SQLite online backup
    source_conn = sqlite3.connect(str(DB_PATH))
    dest_conn = sqlite3.connect(str(temp_target_file))
    try:
        source_conn.backup(dest_conn)
    finally:
        dest_conn.close()
        source_conn.close()

    # 2. Compress with gzip
    with open(temp_target_file, "rb") as f_in:
        with gzip.open(final_gzip_file, "wb", compresslevel=9) as f_out:
            shutil.copyfileobj(f_in, f_out)

    # 3. Remove raw temp db file
    temp_target_file.unlink(missing_ok=True)

    elapsed = round(time.time() - start_time, 2)
    size_kb = round(final_gzip_file.stat().st_size / 1024, 1)
    print(f"[SUCCESS] Backup saved: {final_gzip_file} ({size_kb} KB) in {elapsed}s")

    # 4. Clean up backups older than RETENTION_DAYS
    cutoff_time = time.time() - (RETENTION_DAYS * 86400)
    purged_count = 0
    for file in BACKUP_DIR.glob("sixsense_*.db.gz"):
        if file.stat().st_mtime < cutoff_time:
            file.unlink(missing_ok=True)
            purged_count += 1

    if purged_count > 0:
        print(f"[CLEANUP] Purged {purged_count} backups older than {RETENTION_DAYS} days.")

if __name__ == "__main__":
    perform_backup()
