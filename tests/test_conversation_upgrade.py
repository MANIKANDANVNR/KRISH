from storage.database import Database
from storage.repository import Repository
from memory.manager import MemoryManager


def test_multiple_conversations_are_isolated(tmp_path):
    db = Database(tmp_path / "test.db")
    repo = Repository(db)
    memory = MemoryManager(repo)

    first = memory.create_conversation("First")
    memory.add_message("user", "hello first")
    second = memory.create_conversation("Second")
    memory.add_message("user", "hello second")

    assert [m["content"] for m in repo.get_messages(conversation_id=first)] == ["hello first"]
    assert [m["content"] for m in repo.get_messages(conversation_id=second)] == ["hello second"]
    assert len(repo.list_conversations()) == 2
    db.close()


def test_existing_messages_migrate_to_default(tmp_path):
    db = Database(tmp_path / "test.db")
    repo = Repository(db)
    repo.save_message("user", "old message")
    db.close()

    db2 = Database(tmp_path / "test.db")
    repo2 = Repository(db2)
    assert repo2.get_messages(conversation_id="default")[0]["content"] == "old message"
    assert repo2.list_conversations()
    db2.close()
