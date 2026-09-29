from agent.task import Task


class Agent:

    def __init__(
        self,
        planner,
        validator,
        executor,
        verifier,
        recovery,
        reporter,
    ):

        self.planner = planner
        self.validator = validator
        self.executor = executor
        self.verifier = verifier
        self.recovery = recovery
        self.reporter = reporter

    def run(
        self,
        description,
        session_id=None,
    ):

        try:

            task = Task(
                description
            )

            plan = self.planner.plan(
                task
            )

            self.validator.validate(
                plan
            )

            result = None

            for step in plan:

                result = self.executor.execute(
                    step,
                    session_id,
                )

                if not self.verifier.verify(
                    result
                ):
                    raise RuntimeError(
                        "Verification failed."
                    )

            return self.reporter.success(
                result
            )

        except Exception as error:

            return self.recovery.recover(
                error
            )