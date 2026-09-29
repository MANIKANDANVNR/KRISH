class LongTermMemory:

    def __init__(self, repository=None):

        self.repository = repository

        self.data = {}

    def set(
        self,
        key,
        value,
    ):

        self.data[key] = value

        if self.repository:

            self.repository.save_memory(
                "long_term",
                value,
                key,
            )

    def get(
        self,
        key,
        default=None,
    ):

        if key in self.data:
            return self.data[key]

        return default