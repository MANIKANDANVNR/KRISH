class PlanValidator:

    REQUIRED = {
        "id",
        "action",
    }

    def validate(self, plan):

        if not isinstance(
            plan,
            list,
        ):
            raise ValueError(
                "Plan must be a list."
            )

        if not plan:
            raise ValueError(
                "Plan cannot be empty."
            )

        ids = set()

        for step in plan:

            if not isinstance(
                step,
                dict,
            ):
                raise ValueError(
                    "Invalid plan step."
                )

            missing = (
                self.REQUIRED
                - set(step)
            )

            if missing:
                raise ValueError(
                    f"Missing: {missing}"
                )

            if step["id"] in ids:
                raise ValueError(
                    "Duplicate step ID."
                )

            ids.add(step["id"])

        return True