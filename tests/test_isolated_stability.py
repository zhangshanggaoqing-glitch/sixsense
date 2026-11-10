"""Isolated stability tests. They create a temporary SQLite file and never open the repo database."""

import os
import sqlite3
import tempfile
import unittest
from pathlib import Path

TMP = tempfile.mkdtemp(prefix="sixsense-isolated-")
os.environ["SIX_SENSE_DATA_DIR"] = TMP
os.environ["JWT_SECRET"] = "isolated-test-secret"
os.environ["CET6_RAW_SOURCE_DIR"] = TMP

REPO_DB = Path("/workspace/data/sixsense.db")
REPO_DB_BEFORE = (REPO_DB.stat().st_size, REPO_DB.stat().st_mtime_ns) if REPO_DB.exists() else None

from fastapi.testclient import TestClient  # noqa: E402
from backend.app.database import DB_PATH, init_db  # noqa: E402
from backend.app.main import app  # noqa: E402

GUEST = {"X-Guest-Id": "gst_isolatedtest01"}


def _repo_db_unchanged() -> bool:
    if REPO_DB_BEFORE is None:
        return not REPO_DB.exists()
    return (REPO_DB.stat().st_size, REPO_DB.stat().st_mtime_ns) == REPO_DB_BEFORE


class IsolatedStabilityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        assert Path(DB_PATH).resolve().is_relative_to(Path(TMP).resolve())
        assert Path(DB_PATH).resolve() != REPO_DB.resolve()
        init_db()
        conn = sqlite3.connect(DB_PATH)
        now = 1_700_000_000
        conn.execute(
            """
            INSERT INTO vocab_frequency
                (word, frequency, exam_count, phonetic, pos, definition_zh, examples_json)
            VALUES ('alpha', 12, 3, 'ˈælfə', 'n.', '合成词', '[]')
            """
        )
        conn.execute(
            """
            INSERT INTO user_vocab_srs
                (user_id, word, state, stability, difficulty, reps, lapses, last_review, due, quiz_fails, updated_at)
            VALUES
                ('gst_isolatedtest01', 'alpha', 'review', 2.0, 5.0, 3, 0, ?, ?, 0, ?),
                ('gst_isolatedtest01', 'orphan', 'review', 1.0, 5.0, 2, 0, ?, ?, 0, ?)
            """,
            (now - 100, now - 10, now, now - 100, now - 20, now),
        )
        conn.commit()
        conn.close()
        cls.client = TestClient(app)
        assert _repo_db_unchanged()

    @classmethod
    def tearDownClass(cls):
        cls.client.close()
        assert _repo_db_unchanged()

    def test_resume_roundtrip_keeps_sentence_four(self):
        payload = {
            "exam_id": "synthetic-set",
            "subpart_id": "synthetic-lesson",
            "sentence_index": 3,
            "has_progress": True,
            "is_completed": False,
        }
        first = self.client.post("/api/progress/resume", json=payload, headers=GUEST)
        second = self.client.post("/api/progress/resume", json=payload, headers=GUEST)
        self.assertEqual(first.status_code, 200)
        self.assertEqual(second.status_code, 200)
        body = self.client.get("/api/progress/resume", headers=GUEST).json()
        self.assertEqual(body["sentence_index"], 3)
        self.assertEqual(body["subpart_id"], "synthetic-lesson")
        conn = sqlite3.connect(DB_PATH)
        count = conn.execute(
            "SELECT COUNT(*) FROM user_state WHERE key = ?",
            ("resume:gst_isolatedtest01",),
        ).fetchone()[0]
        conn.close()
        self.assertEqual(count, 1)

    def test_server_resume_is_last_write_wins_without_a_new_rule(self):
        """The sentence-4 guard is in the client. The API still stores an explicit 0."""
        self.client.post(
            "/api/progress/resume",
            json={"exam_id": "synthetic-set", "subpart_id": "synthetic-lesson", "sentence_index": 3, "has_progress": True},
            headers=GUEST,
        )
        moved = self.client.post(
            "/api/progress/resume",
            json={"exam_id": "synthetic-set", "subpart_id": "synthetic-lesson", "sentence_index": 0, "has_progress": True},
            headers=GUEST,
        )
        self.assertEqual(moved.status_code, 200)
        self.assertEqual(self.client.get("/api/progress/resume", headers=GUEST).json()["sentence_index"], 0)

    def test_missing_exam_does_not_drop_saved_resume(self):
        self.client.post(
            "/api/progress/resume",
            json={"exam_id": "synthetic-set", "subpart_id": "synthetic-lesson", "sentence_index": 3, "has_progress": True},
            headers=GUEST,
        )
        missing = self.client.get("/api/exams/does-not-exist")
        self.assertEqual(missing.status_code, 404)
        self.assertEqual(self.client.get("/api/progress/resume", headers=GUEST).json()["sentence_index"], 3)

    def test_due_card_missing_from_frequency_table_stays_in_the_session(self):
        body = self.client.get("/api/vocab/session", headers=GUEST).json()
        words = {item["word"]: item for item in body["items"]}
        self.assertIn("alpha", words)
        self.assertIn("orphan", words)
        self.assertTrue(words["orphan"]["is_review"])
        self.assertFalse(body["is_completed"])
        summary = self.client.get("/api/vocab/summary", headers=GUEST).json()
        self.assertGreaterEqual(summary["due_count"], 2)

    def test_zero_heartbeat_does_not_add_time_and_retries_are_not_idempotent(self):
        """Documents the current rule: a second successful heartbeat adds time again.
        There is no idempotency key, and this test does not change that rule.
        """
        idle = self.client.post(
            "/api/progress/heartbeat",
            json={"exam_id": "synthetic-set", "active_seconds": 0},
            headers=GUEST,
        )
        self.assertEqual(idle.status_code, 200)
        self.assertEqual(idle.json()["active_seconds"], 0)
        self.client.post(
            "/api/progress/heartbeat",
            json={"exam_id": "synthetic-set", "active_seconds": 10, "completed_sentence": False},
            headers=GUEST,
        )
        self.client.post(
            "/api/progress/heartbeat",
            json={"exam_id": "synthetic-set", "active_seconds": 10, "completed_sentence": False},
            headers=GUEST,
        )
        conn = sqlite3.connect(DB_PATH)
        row = conn.execute(
            "SELECT COALESCE(SUM(active_seconds), 0) FROM listening_sessions WHERE user_id = ?",
            ("gst_isolatedtest01",),
        ).fetchone()
        conn.close()
        self.assertEqual(row[0], 20)


if __name__ == "__main__":
    unittest.main()
