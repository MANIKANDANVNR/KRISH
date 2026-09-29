from brain.brain import Brain
from memory.manager import MemoryManager


class FakeProvider:
    def stream(self, messages):
        yield "Hello"
        yield " KRISH"

    def generate(self, messages):
        return "Hello KRISH"


class FakeRouter:
    def select(self):
        return FakeProvider()


def test_brain_stream_persists_complete_response():
    memory = MemoryManager()
    brain = Brain(FakeRouter(), memory, None)
    chunks = list(brain.stream("hello"))
    assert "".join(chunks) == "Hello KRISH"
    assert memory.conversation.recent()[-2:] == [
        {"role": "user", "content": "hello"},
        {"role": "assistant", "content": "Hello KRISH"},
    ]
