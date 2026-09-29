class WorkingMemory:

    def __init__(self, limit=30):

        self.limit = limit
        self.items = []

    def add(self, item):

        self.items.append(item)

        if len(self.items) > self.limit:

            self.items = self.items[
                -self.limit:
            ]

    def clear(self):
        self.items.clear()

    def recent(self, limit=None):

        if limit is None:
            limit = self.limit

        return self.items[-limit:]