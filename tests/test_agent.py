from agent.agent import Agent
from agent.executor import Executor
from agent.plan_validator import PlanValidator
from agent.planner import Planner
from agent.recovery import Recovery
from agent.reporter import Reporter
from agent.verifier import Verifier


class FakeSecurity:

    def authorize(
        self,
        *args,
        **kwargs,
    ):
        return True


class FakeTools:

    def get(self, name):
        raise KeyError(name)


def test_agent():

    agent = Agent(
        Planner(),
        PlanValidator(),
        Executor(
            FakeTools(),
            FakeSecurity(),
        ),
        Verifier(),
        Recovery(),
        Reporter(),
    )

    result = agent.run(
        "Hello KRISH"
    )

    assert result["success"]

    assert result["result"] == (
        "Hello KRISH"
    )