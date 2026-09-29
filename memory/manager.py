class MemoryManager:
    def __init__(self, repository=None, working_limit=30):
        from memory.conversation import ConversationMemory
        from memory.episodic import EpisodicMemory
        from memory.long_term import LongTermMemory
        from memory.retrieval import MemoryRetriever
        from memory.working import WorkingMemory
        self.working = WorkingMemory(working_limit)
        self.conversation = ConversationMemory()
        self.long_term = LongTermMemory(repository)
        self.episodic = EpisodicMemory()
        self.retriever = MemoryRetriever()
        self.repository = repository
        if repository:
            conversations = repository.list_conversations()
            if conversations:
                self.load_conversation(conversations[0]["conversation_id"])

    @property
    def conversation_id(self):
        return self.conversation.conversation_id

    def create_conversation(self, title="New Chat"):
        conversation_id = self.repository.create_conversation(title) if self.repository else "default"
        self.conversation.load(conversation_id, [])
        self.working.items.clear()
        return conversation_id

    def load_conversation(self, conversation_id):
        messages = self.repository.get_messages(conversation_id=conversation_id) if self.repository else []
        self.conversation.load(conversation_id, messages)
        self.working.items.clear()
        for message in messages[-30:]:
            self.working.add(message)
        return messages

    def list_conversations(self):
        return self.repository.list_conversations() if self.repository else []

    def rename_conversation(self, conversation_id, title):
        if self.repository:
            self.repository.rename_conversation(conversation_id, title)

    def delete_conversation(self, conversation_id):
        if self.repository:
            self.repository.delete_conversation(conversation_id)
        if self.conversation_id == conversation_id:
            self.create_conversation()

    def add_message(self, role, content):
        self.conversation.add(role, content)
        self.working.add({"role": role, "content": content})
        if self.repository:
            self.repository.save_message(role, content, self.conversation_id)

    def remember(self, value, category="general", key=None):
        if self.repository:
            self.repository.save_memory(category, value, key)
        self.working.add(value)

    def retrieve(self, query, limit=8):
        candidates = list(self.working.items)
        if self.repository:
            candidates.extend(row["value"] for row in self.repository.get_memories())
        return self.retriever.search(candidates, query, limit)
