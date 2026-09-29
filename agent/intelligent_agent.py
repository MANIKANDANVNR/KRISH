from agent.intent import IntentRouter
from agent.executor import ApprovalRequired


class IntelligentAgent:

    def __init__(
        self,
        agent,
        intent_router=None,
    ):

        self.agent = agent

        self.intent_router = (
            intent_router
            or IntentRouter()
        )

    def handle(
        self,
        user_input,
        session_id,
        request_id=None,
    ):

        intent = self.intent_router.detect(
            user_input
        )

        if not intent.requires_tool:

            return {
                "type": "conversation",
                "intent": intent,
                "result": None,
            }

        step = {
            "id": 1,
            "action": intent.name,
            **self._arguments_to_step(
                intent
            ),
        }

        try:

            result = (
                self.agent.executor.execute(
                    step,
                    session_id=session_id,
                    request_id=request_id,
                )
            )

        except ApprovalRequired as approval:

            return {
                "type": "approval_required",
                "intent": intent,
                "step": step,
                "request_id": approval.request_id,
                "permission": approval.permission,
                "reason": approval.reason,
            }

        if not self.agent.verifier.verify(
            result
        ):

            raise RuntimeError(
                "Tool result verification failed."
            )

        return {
            "type": "tool",
            "intent": intent,
            "result": result,
        }

    @staticmethod
    def _arguments_to_step(intent):

        arguments = intent.arguments

        if intent.name == "calculator":

            return {
                "input": arguments[
                    "expression"
                ]
            }

        if intent.name == "python":

            return {
                "input": arguments[
                    "expression"
                ]
            }

        if intent.name == "file.read":

            return {
                "path": arguments[
                    "path"
                ]
            }

        if intent.name == "file.write":

            return {
                "path": arguments[
                    "path"
                ],
                "content": arguments[
                    "content"
                ],
            }

        if intent.name == "web.get":

            return {
                "url": arguments[
                    "url"
                ]
            }

        return {}