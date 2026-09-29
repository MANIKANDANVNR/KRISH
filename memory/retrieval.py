class MemoryRetriever:

    def search(
        self,
        memories,
        query,
        limit=10,
    ):

        query_words = {
            word.lower()
            for word in query.split()
            if len(word) > 2
        }

        scored = []

        for memory in memories:

            text = str(memory).lower()

            score = sum(
                word in text
                for word in query_words
            )

            if score:

                scored.append(
                    (score, memory)
                )

        scored.sort(
            key=lambda item: item[0],
            reverse=True,
        )

        return [
            item[1]
            for item in scored[:limit]
        ]