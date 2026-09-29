class ConversationMemory:
    def __init__(self):
        self.messages = []
        self.conversation_id = "default"

    def load(self, conversation_id, messages):
        self.conversation_id = conversation_id
        self.messages = [
            {"role": message["role"], "content": message["content"]}
            for message in messages
        ]

    def add(self, role, content):
        self.messages.append({"role": role, "content": content})

    def recent(self, limit=30):
        return self.messages[-limit:]

    def clear(self):
        self.messages.clear()
