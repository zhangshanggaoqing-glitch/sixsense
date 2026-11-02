import sqlite3
import json
from pathlib import Path
from backend.app.config import DB_PATH

def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA synchronous = NORMAL;")
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # 1. Exams
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS exams (
        id TEXT PRIMARY KEY,
        year INTEGER NOT NULL,
        month INTEGER NOT NULL,
        set_number INTEGER NOT NULL,
        title TEXT NOT NULL,
        audio_file TEXT NOT NULL,
        audio_duration REAL NOT NULL DEFAULT 0.0,
        is_golden INTEGER NOT NULL DEFAULT 0
    );
    """)

    # 2. Sections
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sections (
        id TEXT PRIMARY KEY,
        exam_id TEXT NOT NULL,
        type TEXT NOT NULL,
        title TEXT NOT NULL,
        order_num INTEGER NOT NULL,
        FOREIGN KEY (exam_id) REFERENCES exams(id)
    );
    """)

    # 3. Subparts (e.g. Conversation 1, Passage 1)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS subparts (
        id TEXT PRIMARY KEY,
        section_id TEXT NOT NULL,
        exam_id TEXT NOT NULL,
        type TEXT NOT NULL,
        title TEXT NOT NULL,
        order_num INTEGER NOT NULL,
        start_time REAL NOT NULL DEFAULT 0.0,
        end_time REAL NOT NULL DEFAULT 0.0,
        questions_json TEXT DEFAULT '[]',
        FOREIGN KEY (section_id) REFERENCES sections(id),
        FOREIGN KEY (exam_id) REFERENCES exams(id)
    );
    """)

    # 4. Sentences
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sentences (
        id TEXT PRIMARY KEY,
        exam_id TEXT NOT NULL,
        section_id TEXT NOT NULL,
        subpart_id TEXT NOT NULL,
        order_num INTEGER NOT NULL,
        speaker TEXT DEFAULT '',
        start_time REAL NOT NULL,
        end_time REAL NOT NULL,
        english TEXT NOT NULL,
        chinese TEXT NOT NULL,
        words_json TEXT DEFAULT '[]',
        confidence REAL DEFAULT 1.0,
        FOREIGN KEY (exam_id) REFERENCES exams(id),
        FOREIGN KEY (section_id) REFERENCES sections(id),
        FOREIGN KEY (subpart_id) REFERENCES subparts(id)
    );
    """)

    # 5. Vocabulary
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vocabulary (
        id TEXT PRIMARY KEY,
        word TEXT NOT NULL,
        lemma TEXT NOT NULL,
        phonetic TEXT DEFAULT '',
        part_of_speech TEXT DEFAULT '',
        definition_zh TEXT DEFAULT '',
        cet_level TEXT DEFAULT 'CET-6',
        source_sentence_id TEXT,
        source_sentence_en TEXT,
        source_sentence_zh TEXT,
        exam_id TEXT,
        audio_clip_start REAL,
        audio_clip_end REAL,
        created_at REAL NOT NULL,
        review_count INTEGER DEFAULT 0,
        mastery REAL DEFAULT 0.0
    );
    """)

    # 6. Dictation Attempts
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS dictation_attempts (
        id TEXT PRIMARY KEY,
        sentence_id TEXT NOT NULL,
        user_input TEXT NOT NULL,
        standard_text TEXT NOT NULL,
        accuracy_score REAL NOT NULL,
        diff_json TEXT NOT NULL,
        created_at REAL NOT NULL
    );
    """)

    # 7. Listening Sessions
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS listening_sessions (
        id TEXT PRIMARY KEY,
        start_time REAL NOT NULL,
        end_time REAL NOT NULL,
        active_seconds INTEGER NOT NULL,
        exam_id TEXT NOT NULL,
        sentences_played INTEGER DEFAULT 0,
        sentences_repeated INTEGER DEFAULT 0,
        dictation_attempts INTEGER DEFAULT 0,
        new_words_count INTEGER DEFAULT 0
    );
    """)

    # 8. User State (Key-Value: last_resume, settings)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_state (
        key TEXT PRIMARY KEY,
        value_json TEXT NOT NULL,
        updated_at REAL NOT NULL
    );
    """)

    # 9. Dictionary Cache
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS dictionary_cache (
        word TEXT PRIMARY KEY,
        data_json TEXT NOT NULL,
        updated_at REAL NOT NULL
    );
    """)

    # 10. Users Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        created_at REAL NOT NULL,
        last_login_at REAL
    );
    """)

    # 11. Vocab Frequency (CET-6 listening frequency table)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vocab_frequency (
        word TEXT PRIMARY KEY,
        frequency INTEGER NOT NULL DEFAULT 1,
        exam_count INTEGER NOT NULL DEFAULT 1,
        phonetic TEXT DEFAULT '',
        phonetic_uk TEXT DEFAULT '',
        phonetic_us TEXT DEFAULT '',
        pos TEXT DEFAULT '',
        definition_zh TEXT DEFAULT '',
        tags_json TEXT DEFAULT '[]',
        examples_json TEXT DEFAULT '[]'
    );
    """)
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_vocab_freq_count ON vocab_frequency(frequency DESC);")

    # 12. User Vocab Status (Track mastery: known / learning)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_vocab_status (
        user_id TEXT NOT NULL,
        word TEXT NOT NULL,
        status TEXT NOT NULL,
        updated_at REAL NOT NULL,
        PRIMARY KEY (user_id, word)
    );
    """)
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_user_vocab_status ON user_vocab_status(user_id, status);")

    # 13. Vocab Distractors (Precomputed listening distractors for 4-choice quiz)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vocab_distractors (
        word TEXT PRIMARY KEY,
        distractors_json TEXT NOT NULL,
        quality TEXT NOT NULL
    );
    """)

    # 14. User Vocab SRS (FSRS-5 memory curve state)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_vocab_srs (
        user_id TEXT NOT NULL,
        word TEXT NOT NULL,
        state TEXT NOT NULL DEFAULT 'new',
        stability REAL NOT NULL DEFAULT 0.0,
        difficulty REAL NOT NULL DEFAULT 0.0,
        reps INTEGER NOT NULL DEFAULT 0,
        lapses INTEGER NOT NULL DEFAULT 0,
        last_review REAL DEFAULT NULL,
        due REAL NOT NULL DEFAULT 0.0,
        rating INTEGER DEFAULT NULL,
        quiz_fails INTEGER NOT NULL DEFAULT 0,
        updated_at REAL NOT NULL,
        PRIMARY KEY (user_id, word)
    );
    """)
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_user_srs_due ON user_vocab_srs(user_id, due ASC);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_user_srs_state ON user_vocab_srs(user_id, state);")

    # 15. User Vocab Settings (Daily new quota, autoplay, etc.)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_vocab_settings (
        user_id TEXT PRIMARY KEY,
        daily_new_quota INTEGER NOT NULL DEFAULT 20,
        autoplay_audio INTEGER NOT NULL DEFAULT 1,
        algorithm_version TEXT NOT NULL DEFAULT 'FSRS-5.0.0',
        updated_at REAL NOT NULL
    );
    """)

    # 16. Vocab Telemetry Events (Minimal event logging)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vocab_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL,
        event_name TEXT NOT NULL,
        word TEXT DEFAULT '',
        payload_json TEXT DEFAULT '{}',
        created_at REAL NOT NULL
    );
    """)
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_vocab_events_user ON vocab_events(user_id, created_at DESC);")

    # Ensure vocabulary table has UK/US phonetic & audio fields, plus user_id
    cursor.execute("PRAGMA table_info(vocabulary);")
    vocab_cols = [r[1] for r in cursor.fetchall()]
    for col in ["phonetic_uk", "phonetic_us", "audio_uk", "audio_us"]:
        if col not in vocab_cols:
            cursor.execute(f"ALTER TABLE vocabulary ADD COLUMN {col} TEXT DEFAULT '';")
    if "user_id" not in vocab_cols:
        cursor.execute("ALTER TABLE vocabulary ADD COLUMN user_id TEXT DEFAULT 'default';")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_vocab_user ON vocabulary(user_id);")

    # Ensure dictation_attempts has user_id
    cursor.execute("PRAGMA table_info(dictation_attempts);")
    dict_cols = [r[1] for r in cursor.fetchall()]
    if "user_id" not in dict_cols:
        cursor.execute("ALTER TABLE dictation_attempts ADD COLUMN user_id TEXT DEFAULT 'default';")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_dict_user ON dictation_attempts(user_id);")

    # Ensure listening_sessions has user_id
    cursor.execute("PRAGMA table_info(listening_sessions);")
    sess_cols = [r[1] for r in cursor.fetchall()]
    if "user_id" not in sess_cols:
        cursor.execute("ALTER TABLE listening_sessions ADD COLUMN user_id TEXT DEFAULT 'default';")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_sess_user ON listening_sessions(user_id);")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully at", DB_PATH)
