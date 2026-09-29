import json
import uuid
from datetime import datetime, timezone


def utc_now():
    return datetime.now(timezone.utc).isoformat()


class Repository:
    def __init__(self, database):
        self.db = database

    def save_memory(self, category, value, key=None):
        self.db.execute("""
            INSERT INTO memory(category, key, value, created_at)
            VALUES (?, ?, ?, ?)
        """, (category, key, json.dumps(value, ensure_ascii=False), utc_now()))

    def get_memories(self, category=None):
        if category:
            cursor = self.db.execute("SELECT * FROM memory WHERE category=? ORDER BY id DESC", (category,))
        else:
            cursor = self.db.execute("SELECT * FROM memory ORDER BY id DESC")
        return [dict(row) for row in cursor.fetchall()]

    def create_conversation(self, title="New Chat"):
        conversation_id = uuid.uuid4().hex
        now = utc_now()
        self.db.execute("""
            INSERT INTO conversation_sessions(conversation_id, title, created_at, updated_at)
            VALUES (?, ?, ?, ?)
        """, (conversation_id, title.strip() or "New Chat", now, now))
        return conversation_id

    def ensure_conversation(self, conversation_id, title="New Chat"):
        row = self.db.execute(
            "SELECT conversation_id FROM conversation_sessions WHERE conversation_id=?",
            (conversation_id,),
        ).fetchone()
        if row is None:
            now = utc_now()
            self.db.execute("""
                INSERT INTO conversation_sessions(conversation_id, title, created_at, updated_at)
                VALUES (?, ?, ?, ?)
            """, (conversation_id, title.strip() or "New Chat", now, now))

    def rename_conversation(self, conversation_id, title):
        self.db.execute(
            "UPDATE conversation_sessions SET title=?, updated_at=? WHERE conversation_id=?",
            (title.strip() or "New Chat", utc_now(), conversation_id),
        )

    def delete_conversation(self, conversation_id):
        self.db.execute("DELETE FROM conversations WHERE conversation_id=?", (conversation_id,))
        self.db.execute("DELETE FROM conversation_sessions WHERE conversation_id=?", (conversation_id,))

    def list_conversations(self):
        cursor = self.db.execute("""
            SELECT conversation_id, title, created_at, updated_at
            FROM conversation_sessions
            ORDER BY updated_at DESC
        """)
        return [dict(row) for row in cursor.fetchall()]

    def save_message(self, role, content, conversation_id="default"):
        self.ensure_conversation(conversation_id)
        now = utc_now()
        self.db.execute("""
            INSERT INTO conversations(role, content, created_at, conversation_id)
            VALUES (?, ?, ?, ?)
        """, (role, content, now, conversation_id))
        if role == "user":
            row = self.db.execute(
                "SELECT title FROM conversation_sessions WHERE conversation_id=?",
                (conversation_id,),
            ).fetchone()
            if row and row[0] in ("New Chat", "Previous Conversation"):
                title = " ".join(content.strip().split())[:60] or "New Chat"
                self.rename_conversation(conversation_id, title)
            else:
                self.db.execute(
                    "UPDATE conversation_sessions SET updated_at=? WHERE conversation_id=?",
                    (now, conversation_id),
                )

    def get_messages(self, limit=50, conversation_id="default"):
        cursor = self.db.execute("""
            SELECT role, content, created_at
            FROM conversations
            WHERE conversation_id=?
            ORDER BY id DESC LIMIT ?
        """, (conversation_id, limit))
        rows = cursor.fetchall()
        return [dict(row) for row in reversed(rows)]

    def set_setting(self, key, value):
        self.db.execute("""
            INSERT INTO settings(key, value, updated_at) VALUES (?, ?, ?)
            ON CONFLICT(key) DO UPDATE SET value=excluded.value, updated_at=excluded.updated_at
        """, (key, json.dumps(value, ensure_ascii=False), utc_now()))

    def get_setting(self, key, default=None):
        row = self.db.execute("SELECT value FROM settings WHERE key=?", (key,)).fetchone()
        if row is None:
            return default
        try:
            return json.loads(row[0])
        except json.JSONDecodeError:
            return row[0]
