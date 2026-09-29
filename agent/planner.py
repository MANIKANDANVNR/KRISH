class Planner:

    def plan(self, task):

        description = (
            task.description.strip()
        )

        if not description:
            raise ValueError(
                "Task description empty."
            )

        return [
            {
                "id": 1,
                "action": "respond",
                "input": description,
            }
        ]