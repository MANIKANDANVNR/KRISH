from agent.executor import Executor
from security.kernel import SecurityKernel
from storage.database import Database
from storage.repository import Repository
from tools.calculator import CalculatorTool
from tools.registry import ToolRegistry


def build():

    database = Database(":memory:")

    repository = Repository(
        database
    )

    security = SecurityKernel(
        repository=repository
    )

    security.initialize()

    security.register_owner(
        "TEST_OWNER",
        "Test Owner",
    )

    security.configure_secret(
        "test-secret"
    )

    assert security.authenticate(
        "test-secret"
    )

    session = security.create_session()

    security.permissions.grant(
        "tool.calculator"
    )

    tools = ToolRegistry()

    tools.register(
        CalculatorTool()
    )

    executor = Executor(
        tools,
        security,
    )

    return (
        database,
        executor,
        session,
    )


def test_calculator_through_security():

    database, executor, session = build()

    try:

        result = executor.execute(
            {
                "id": 1,
                "action": "calculator",
                "input": "((4 + 5) * 557) / 4",
            },
            session_id=session.session_id,
        )

        assert result == 1253.25

    finally:

        database.close()


def test_calculator_requires_session():

    database, executor, _ = build()

    try:

        try:

            executor.execute(
                {
                    "id": 1,
                    "action": "calculator",
                    "input": "4 + 5",
                }
            )

            assert False

        except PermissionError:

            assert True

    finally:

        database.close()