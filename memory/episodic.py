from datetime import datetime, timezone


class EpisodicMemory:

    def __init__(self):
        self.episodes = []

    def add(
        self,
        event,
        metadata=None,
    ):

        episode = {
            "event": event,
            "metadata": metadata or {},
            "timestamp":
                datetime.now(
                    timezone.utc
                ).isoformat(),
        }

        self.episodes.append(
            episode
        )

        return episode

    def recent(self, limit=20):

        return self.episodes[-limit:]