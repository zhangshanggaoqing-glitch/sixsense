#!/usr/bin/env bash
set -e

# ==============================================================================
# Stone Audio (石头听力) - Offsite Backup: Sync Production DB to Local Machine
# ==============================================================================

LOCAL_BACKUP_DIR="$(pwd)/backups/cloud_snapshots"
mkdir -p "$LOCAL_BACKUP_DIR"

echo "=== [1/2] Triggering Atomic Snapshot on Oracle Cloud Server ==="
ssh oracle "python3 /home/ubuntu/sixsense/scripts/backup_db.py"

echo "=== [2/2] Downloading Latest Backups to Local Machine ==="
rsync -avz --progress oracle:/home/ubuntu/backups/db/ "$LOCAL_BACKUP_DIR/"

echo "=== [SUCCESS] Offsite backup complete! Stored in: $LOCAL_BACKUP_DIR ==="
ls -lh "$LOCAL_BACKUP_DIR"
