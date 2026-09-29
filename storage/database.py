import sqlite3
from pathlib import Path


class Database:
    def __init__(self, path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(self.path, check_same_thread=False)
        self.connection.row_factory = sqlite3.Row
        self.initialize()

    def initialize(self):
        cursor = self.connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                key TEXT,
                value TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TEXT NOT NULL,
                conversation_id TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversation_sessions (
                conversation_id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS audit (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                action TEXT NOT NULL,
                result TEXT NOT NULL,
                details TEXT,
                created_at TEXT NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)
        columns = {row[1] for row in cursor.execute("PRAGMA table_info(conversations)").fetchall()}
        if "conversation_id" not in columns:
            cursor.execute("ALTER TABLE conversations ADD COLUMN conversation_id TEXT")
        cursor.execute("SELECT COUNT(*) FROM conversation_sessions")
        if cursor.fetchone()[0] == 0:
            cursor.execute("SELECT COUNT(*) FROM conversations")
            if cursor.fetchone()[0] > 0:
                cursor.execute("""
                    INSERT INTO conversation_sessions(conversation_id, title, created_at, updated_at)
                    VALUES ('default', 'Previous Conversation', datetime('now'), datetime('now'))
                """)
                cursor.execute("UPDATE conversations SET conversation_id='default' WHERE conversation_id IS NULL")
        self.connection.commit()

    def execute(self, query, parameters=()):
        cursor = self.connection.cursor()
        cursor.execute(query, parameters)
        self.connection.commit()
        return cursor

    def close(self):
        if self.connection:
            self.connection.close()
