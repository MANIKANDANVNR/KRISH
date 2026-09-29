from memory.manager import MemoryManager


def test_memory():

    memory = MemoryManager()

    memory.add_message(
        "user",
        "My name is Owner.",
    )

    memory.remember(
        "Python developer",
        category="preference",
    )

    results = memory.retrieve(
        "Python"
    )

    assert results