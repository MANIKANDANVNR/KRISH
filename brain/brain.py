from threading import Event

from brain.context import ContextBuilder
from brain.validation import ResponseValidator


class Brain:

    SYSTEM_PROMPT = """
You are KRISH, a personal AI assistant.

KRISH is a modular local-first AI system.

Rules:
1. Never claim an action was performed unless KRISH actually performed it.
2. Never invent tools or capabilities.
3. Never claim external access unless the corresponding subsystem performed it.
4. Respect owner authentication and authorization.
5. Never autonomously expand authority.
6. Never autonomously modify KRISH source code.
7. Explain uncertainty honestly.
8. Use verified tool results when supplied.
9. Answer naturally, directly, and use previous conversation context when relevant.
"""

    def __init__(
        self,
        router,
        memory,
        repository,
    ):

        self.router = router

        self.memory = memory

        self.repository = repository

        self.context = ContextBuilder()

        self.validator = ResponseValidator()

    # =========================================================
    # MESSAGE BUILDING
    # =========================================================

    def build_messages(
        self,
        user_input,
        tool_result=None,
    ):

        conversation = (
            self.memory.conversation.recent(
                24
            )
        )

        memories = self.memory.retrieve(
            user_input,
            limit=6,
        )

        system_prompt = self.SYSTEM_PROMPT

        if tool_result is not None:

            system_prompt += (
                "\nA KRISH tool has already executed "
                "for this request. "
                "The verified result is below. "
                "Do not pretend you executed it yourself.\n"
                f"TOOL RESULT:\n{tool_result}\n"
            )

        return self.context.build(
            system_prompt,
            conversation,
            memories,
            user_input,
        )

    # =========================================================
    # NORMAL RESPONSE
    # =========================================================

    def respond(
        self,
        user_input,
        tool_result=None,
    ):

        provider = self.router.select()

        response = provider.generate(
            self.build_messages(
                user_input,
                tool_result,
            )
        )

        response = self.validator.validate(
            response
        )

        self.memory.add_message(
            "user",
            user_input,
        )

        self.memory.add_message(
            "assistant",
            response,
        )

        return response

    # =========================================================
    # STREAMING RESPONSE
    # =========================================================

    def stream(
        self,
        user_input,
        tool_result=None,
        cancel_event=None,
    ):

        provider = self.router.select()

        # -----------------------------------------------------
        # Create a cancellation event when the caller does not
        # provide one.
        # -----------------------------------------------------

        if cancel_event is None:

            cancel_event = Event()

        # -----------------------------------------------------
        # Provider without streaming support
        # -----------------------------------------------------

        if not hasattr(
            provider,
            "stream",
        ):

            if cancel_event.is_set():

                return

            response = self.respond(
                user_input,
                tool_result,
            )

            if not cancel_event.is_set():

                yield response

            return

        chunks = []

        try:

            stream = provider.stream(
                self.build_messages(
                    user_input,
                    tool_result,
                )
            )

            for chunk in stream:

                if cancel_event.is_set():

                    # -------------------------------------------------
                    # Tell providers that support cancellation to
                    # terminate their underlying generation.
                    # -------------------------------------------------

                    cancel = getattr(
                        provider,
                        "cancel",
                        None,
                    )

                    if callable(cancel):

                        try:
                            cancel()
                        except Exception:
                            pass

                    break

                text = str(chunk)

                if not text:

                    continue

                chunks.append(text)

                yield text

            # -----------------------------------------------------
            # A cancelled request must never become a completed
            # assistant response.
            # -----------------------------------------------------

            if cancel_event.is_set():

                return

            response = self.validator.validate(
                "".join(chunks)
            )

            self.memory.add_message(
                "user",
                user_input,
            )

            self.memory.add_message(
                "assistant",
                response,
            )

        finally:

            if cancel_event.is_set():

                cancel = getattr(
                    provider,
                    "cancel",
                    None,
                )

                if callable(cancel):

                    try:
                        cancel()
                    except Exception:
                        pass