#!/usr/bin/env python3
"""Offline SQLite backup/restore drill.

Uses the SQLite backup API so a live WAL is included in the snapshot.
Refuses production paths, the repository database, .env files, and media trees.
Does not connect to the production host and does not print row contents.
"""

import argparse
import sqlite3
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
REPO_DB = (REPO_ROOT / "data" / "sixsense.db").resolve()
FORBIDDEN = (
    "/home/ubuntu/sixsense",
    "43.142.98.29",
    "mystone.top",
    "/var/lib/docker",
)


def refuse(path: Path) -> None:
    resolved = str(path.resolve())
    if path.resolve() == REPO_DB:
        raise SystemExit("STOP: refusing to read or write the repository database")
    for marker in FORBIDDEN:
        if marker in resolved:
            raise SystemExit(f"STOP: refusing path that matches production marker {marker}")
    if path.suffix in {".env", ".mp3", ".wav"} or path.name.startswith(".env"):
        raise SystemExit("STOP: refusing a secret or media file")


def snapshot(source: Path, dest: Path) -> None:
    refuse(source)
    refuse(dest)
    src = sqlite3.connect(source)
    dst = sqlite3.connect(dest)
    try:
        src.backup(dst)
    finally:
        dst.close()
        src.close()


def drill(work: Path) -> None:
    refuse(work)
    work.mkdir(parents=True, exist_ok=True)
    db_path = work / "synthetic.db"
    refuse(db_path)
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA wal_autocheckpoint=0")
    conn.execute("CREATE TABLE sample (id INTEGER PRIMARY KEY, value TEXT)")
    conn.execute("INSERT INTO sample (value) VALUES ('before-checkpoint')")
    conn.commit()
    # Keep the next commit in the WAL file instead of folding it into the main db.
    conn.execute("INSERT INTO sample (value) VALUES ('in-wal')")
    conn.commit()
    wal = Path(str(db_path) + "-wal")
    wal_while_open = wal.exists() and wal.stat().st_size > 0
    snapshot_path = work / "synthetic-snapshot.db"
    snapshot(db_path, snapshot_path)
    conn.execute("UPDATE sample SET value = 'mutated'")
    conn.commit()
    conn.close()

    restored = work / "synthetic-restored.db"
    snapshot(snapshot_path, restored)
    check = sqlite3.connect(restored)
    rows = [r[0] for r in check.execute("SELECT value FROM sample ORDER BY id").fetchall()]
    integrity = check.execute("PRAGMA integrity_check").fetchone()[0]
    check.close()
    if rows != ["before-checkpoint", "in-wal"]:
        raise SystemExit(f"STOP: restore drill mismatch {rows}")
    if integrity != "ok":
        raise SystemExit(f"STOP: integrity_check {integrity}")
    if wal.exists() and snapshot_path.stat().st_size <= 0:
        raise SystemExit("STOP: snapshot is empty")
    leaked = list(work.glob(".env")) + list(work.glob("*.mp3"))
    if leaked:
        raise SystemExit("STOP: drill directory contains secrets or media")
    print("RESTORE_DRILL_OK")
    print(f"work={work}")
    print(f"wal_present_while_writer_open={wal_while_open}")
    print(f"snapshot_bytes={snapshot_path.stat().st_size}")
    print("restored_rows=2 integrity=ok")
    print("NOTE synthetic data only; production database was not opened")


def main() -> None:
    parser = argparse.ArgumentParser(description="Offline SQLite restore drill")
    parser.add_argument("--work-dir", default="")
    args = parser.parse_args()
    if args.work_dir:
        work = Path(args.work_dir)
        refuse(work)
    else:
        work = Path(tempfile.mkdtemp(prefix="sixsense-restore-drill-"))
    drill(work)


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as exc:
        print(f"STOP: restore drill failed: {exc}", file=sys.stderr)
        sys.exit(1)
