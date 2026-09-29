from getpass import getpass
import threading
from pathlib import Path

from agent.agent import Agent
from agent.executor import Executor
from agent.intelligent_agent import IntelligentAgent
from agent.intent import IntentRouter
from agent.plan_validator import PlanValidator
from agent.planner import Planner
from agent.recovery import Recovery
from agent.reporter import Reporter
from agent.verifier import Verifier

from brain.brain import Brain
from brain.ollama_provider import OllamaProvider
from brain.router import ModelRouter

from core.configuration import Configuration
from core.runtime import Runtime

from evolution.controller import EvolutionController

from memory.manager import MemoryManager

from observability.health import HealthChecker
from observability.logging import configure_logging

from security.kernel import SecurityKernel

from storage.database import Database
from storage.repository import Repository

from tools.calculator import CalculatorTool
from tools.file_tool import FileTool
from tools.python_tool import PythonTool
from tools.registry import ToolRegistry
from tools.system_tool import SystemTool
from tools.web_tool import WebTool


KRISH_VERSION = "1.0.0"


class Krish:

    def __init__(self):

        self.config = Configuration()

        configure_logging(
            self.config.log_level
        )

        self.runtime = Runtime(
            self.config
        )

        self.database = Database(
            self.config.database
        )

        self.repository = Repository(
            self.database
        )

        self.security = SecurityKernel(
            self.config.session_minutes,
            repository=self.repository,
        )

        self.memory = MemoryManager(
            repository=self.repository,
            working_limit=self.config.max_memory,
        )

        self.tools = ToolRegistry()

        self.router = ModelRouter()

        self.evolution = EvolutionController()

        self.health_checker = HealthChecker()

        self.brain = None

        self.agent = None

        self.intelligent_agent = None

        self.session = None

        self.initialized = False

    # ---------------------------------------------------------
    # INITIALIZATION
    # ---------------------------------------------------------

    def initialize(self):

        self.runtime.initialize()

        self.security.initialize()

        if self.security.owner is None:

            self.security.register_owner(
                "OWNER",
                "Owner",
            )

        self._register_tools()

        ollama = OllamaProvider(
            self.config.ollama_host,
            self.config.ollama_model,
        )

        self.router.register(
            "ollama",
            ollama,
        )

        self.brain = Brain(
            self.router,
            self.memory,
            self.repository,
        )

        self.agent = Agent(
            Planner(),
            PlanValidator(),
            Executor(
                self.tools,
                self.security,
            ),
            Verifier(),
            Recovery(),
            Reporter(),
        )

        self.intelligent_agent = IntelligentAgent(
            self.agent,
            IntentRouter(),
        )

        self.runtime.services.register(
            "security",
            self.security,
        )

        self.runtime.services.register(
            "database",
            self.database,
        )

        self.runtime.services.register(
            "memory",
            self.memory,
        )

        self.runtime.services.register(
            "brain",
            self.brain,
        )

        self.runtime.services.register(
            "agent",
            self.agent,
        )

        self.runtime.services.register(
            "intelligent_agent",
            self.intelligent_agent,
        )

        self.runtime.services.register(
            "tools",
            self.tools,
        )

        self.runtime.services.register(
            "evolution",
            self.evolution,
        )

        if not self.memory.list_conversations():

            self.memory.create_conversation(
                "New Chat"
            )

        self.initialized = True

    # ---------------------------------------------------------
    # TOOL REGISTRATION
    # ---------------------------------------------------------

    def _register_tools(self):

        self.tools.register(
            CalculatorTool()
        )

        self.tools.register(
            FileTool(
                Path("data/workspace")
            )
        )

        self.tools.register(
            PythonTool()
        )

        self.tools.register(
            WebTool()
        )

        self.tools.register(
            SystemTool()
        )

    # ---------------------------------------------------------
    # OWNER AUTHENTICATION
    # ---------------------------------------------------------

    def authenticate_owner(self):

        if not self.initialized:

            raise RuntimeError(
                "KRISH is not initialized."
            )

        print()

        if not self.security.has_configured_secret():

            print(
                "First-time KRISH owner setup"
            )

            while True:

                secret = getpass(
                    "Create owner secret: "
                )

                confirmation = getpass(
                    "Confirm owner secret: "
                )

                if not secret:

                    print(
                        "Secret cannot be empty."
                    )

                    continue

                if secret != confirmation:

                    print(
                        "Secrets do not match."
                    )

                    continue

                break

            self.security.configure_secret(
                secret
            )

        else:

            print(
                "KRISH owner authentication"
            )

            secret = getpass(
                "Enter owner secret: "
            )

        if not self.security.authenticate(
            secret
        ):

            raise PermissionError(
                "Owner authentication failed."
            )

        self.session = (
            self.security.create_session()
        )

    # ---------------------------------------------------------
    # BASIC PERMISSIONS
    # ---------------------------------------------------------

    def grant_basic_permissions(self):

        self.security.permissions.grant(
            "tool.calculator"
        )

    # ---------------------------------------------------------
    # STATUS
    # ---------------------------------------------------------

    def status(self):

        return self.health_checker.check(
            self.runtime,
            self.security,
            self.brain,
        )

    # ---------------------------------------------------------
    # INTERNAL TOOL REQUEST
    # ---------------------------------------------------------

    def _handle_tool_request(
        self,
        user_input,
        request_id=None,
    ):

        if self.intelligent_agent is None:

            raise RuntimeError(
                "KRISH agent is not initialized."
            )

        if self.session is None:

            raise PermissionError(
                "Owner session required."
            )

        return self.intelligent_agent.handle(
            user_input,
            self.session.session_id,
            request_id=request_id,
        )

    # ---------------------------------------------------------
    # CONVERSATION MANAGEMENT
    # ---------------------------------------------------------

    @property
    def conversation_id(self):

        return self.memory.conversation_id

    def list_conversations(self):

        return self.memory.list_conversations()

    def load_conversation(
        self,
        conversation_id,
    ):

        return self.memory.load_conversation(
            conversation_id
        )

    def new_conversation(self):

        return self.memory.create_conversation(
            "New Chat"
        )

    def rename_conversation(
        self,
        conversation_id,
        title,
    ):

        self.memory.rename_conversation(
            conversation_id,
            title,
        )

    def delete_conversation(
        self,
        conversation_id,
    ):

        self.memory.delete_conversation(
            conversation_id
        )

    # ---------------------------------------------------------
    # STREAMING CHAT
    # ---------------------------------------------------------

    def stream_chat_message(
        self,
        user_input,
        cancel_event=None,
    ):

        if not self.initialized:

            raise RuntimeError(
                "KRISH is not initialized."
            )

        if self.session is None:

            raise PermissionError(
                "Owner authentication required."
            )

        user_input = user_input.strip()

        if not user_input:

            return

        # -----------------------------------------------------
        # Tool/agent execution happens before model generation.
        #
        # The existing security architecture remains unchanged:
        # tool execution must pass through the agent/security layer.
        # -----------------------------------------------------

        tool_result = self._handle_tool_request(
            user_input
        )

        if (
            tool_result["type"]
            == "approval_required"
        ):

            raise PermissionError(
                "This action requires owner approval."
            )

        # -----------------------------------------------------
        # A cancellation received before model generation
        # prevents unnecessary model execution.
        # -----------------------------------------------------

        if cancel_event is not None:

            if cancel_event.is_set():

                return

        result = (
            tool_result.get("result")
            if tool_result["type"] == "tool"
            else None
        )

        # -----------------------------------------------------
        # REAL CANCELLATION PATH
        #
        # GUI
        #   ↓
        # ChatController
        #   ↓
        # cancel_event
        #   ↓
        # Krish.stream_chat_message
        #   ↓
        # Brain.stream
        #   ↓
        # OllamaProvider.stream
        #   ↓
        # Ollama cancellation
        # -----------------------------------------------------

        yield from self.brain.stream(
            user_input,
            result,
            cancel_event=cancel_event,
        )

    # ---------------------------------------------------------
    # MODEL WARMUP
    # ---------------------------------------------------------

    def warmup_model(self):

        try:

            provider = self.router.select()

            warmup = getattr(
                provider,
                "warmup",
                None,
            )

            if warmup:

                threading.Thread(
                    target=warmup,
                    daemon=True,
                ).start()

        except Exception:

            pass

    # ---------------------------------------------------------
    # GUI CHAT INTERFACE
    # ---------------------------------------------------------

    def handle_chat_message(
        self,
        user_input,
    ):

        if not self.initialized:

            raise RuntimeError(
                "KRISH is not initialized."
            )

        if self.session is None:

            raise PermissionError(
                "Owner authentication required."
            )

        user_input = user_input.strip()

        if not user_input:

            return ""

        tool_result = self._handle_tool_request(
            user_input
        )

        if (
            tool_result["type"]
            == "approval_required"
        ):

            raise PermissionError(
                "This action requires owner approval."
            )

        if (
            tool_result["type"]
            == "tool"
        ):

            return self.brain.respond(
                user_input,
                tool_result["result"],
            )

        return self.brain.respond(
            user_input
        )

    # ---------------------------------------------------------
    # GUI / FUTURE APPROVAL SUPPORT
    # ---------------------------------------------------------

    def request_tool_action(
        self,
        user_input,
    ):

        if not self.initialized:

            raise RuntimeError(
                "KRISH is not initialized."
            )

        if self.session is None:

            raise PermissionError(
                "Owner authentication required."
            )

        return self._handle_tool_request(
            user_input
        )

    # ---------------------------------------------------------
    # APPROVAL REQUEST
    # ---------------------------------------------------------

    def _request_owner_approval(
        self,
        approval_result,
    ):

        request_id = (
            approval_result["request_id"]
        )

        permission = (
            approval_result["permission"]
        )

        reason = (
            approval_result["reason"]
        )

        print()

        print(
            "=" * 70
        )

        print(
            "KRISH APPROVAL REQUIRED"
        )

        print(
            "=" * 70
        )

        print(
            f"Permission: {permission}"
        )

        print(
            f"Reason: {reason}"
        )

        print(
            "Risk: HIGH / CRITICAL"
        )

        print(
            "Approval: ONE-TIME"
        )

        print(
            "Expiration: 60 seconds"
        )

        print(
            "-" * 70
        )

        print(
            "Approve this specific action?"
        )

        print(
            "Type 'yes' to approve."
        )

        print(
            "Type 'no' to cancel."
        )

        answer = input(
            "Approval: "
        ).strip().lower()

        if answer in (
            "yes",
            "y",
        ):

            try:

                self.security.approvals.approve(
                    request_id,
                    self.session.session_id,
                )

            except Exception as error:

                self.security.audit.record(
                    "approval",
                    "approval_failed",
                    permission=permission,
                    request_id=request_id,
                    error=str(error),
                )

                print(
                    f"\nKRISH ERROR: "
                    f"Approval failed: {error}"
                )

                return False

            self.security.audit.record(
                "approval",
                "owner_approved",
                permission=permission,
                request_id=request_id,
            )

            print(
                "\nKRISH: Approval accepted."
            )

            return True

        self.security.approvals.revoke(
            request_id,
            self.session.session_id,
        )

        self.security.audit.record(
            "approval",
            "owner_denied",
            permission=permission,
            request_id=request_id,
        )

        print(
            "\nKRISH: Action cancelled."
        )

        return False

    # ---------------------------------------------------------
    # TERMINAL CHAT
    # ---------------------------------------------------------

    def chat(self):

        if self.session is None:

            raise PermissionError(
                "Owner session required."
            )

        print()

        print(
            "KRISH interactive mode"
        )

        print(
            "Type 'exit' to stop."
        )

        print(
            "Type 'status' to inspect KRISH."
        )

        print(
            "Protected actions require explicit approval."
        )

        while True:

            try:

                user_input = input(
                    "\nYou: "
                ).strip()

            except (
                KeyboardInterrupt,
                EOFError,
            ):

                print()

                break

            if not user_input:

                continue

            if user_input.lower() == "exit":

                break

            if user_input.lower() == "status":

                print(
                    self.status()
                )

                continue

            try:

                tool_result = (
                    self._handle_tool_request(
                        user_input
                    )
                )

                if (
                    tool_result["type"]
                    == "approval_required"
                ):

                    approved = (
                        self._request_owner_approval(
                            tool_result
                        )
                    )

                    if not approved:

                        continue

                    tool_result = (
                        self._handle_tool_request(
                            user_input,
                            request_id=(
                                tool_result[
                                    "request_id"
                                ]
                            ),
                        )
                    )

                    if (
                        tool_result["type"]
                        != "tool"
                    ):

                        print(
                            "\nKRISH ERROR: "
                            "Approved action did "
                            "not execute."
                        )

                        continue

                if (
                    tool_result["type"]
                    == "tool"
                ):

                    response = (
                        self.brain.respond(
                            user_input,
                            tool_result["result"],
                        )
                    )

                else:

                    response = (
                        self.brain.respond(
                            user_input
                        )
                    )

                print(
                    f"\nKRISH: {response}"
                )

            except Exception as error:

                print(
                    f"\nKRISH ERROR: {error}"
                )

    # ---------------------------------------------------------
    # SHUTDOWN
    # ---------------------------------------------------------

    def shutdown(self):

        try:

            if (
                self.runtime.lifecycle.state.value
                != "shutdown"
            ):

                self.runtime.shutdown()

        finally:

            self.database.close()


# =============================================================
# TERMINAL ENTRY POINT
# =============================================================

def main():

    krish = Krish()

    try:

        krish.initialize()

        print()

        print(
            "=" * 70
        )

        print(
            "KRISH PERSONAL AI SYSTEM"
        )

        print(
            "=" * 70
        )

        print(
            f"Version: {KRISH_VERSION}"
        )

        print(
            "Architecture: "
            "Modular AI Agent Platform"
        )

        print(
            "Security: ACTIVE"
        )

        print(
            "Evolution: OWNER CONTROLLED"
        )

        print(
            "Authority Expansion: DISABLED"
        )

        print(
            "Self Modification: DISABLED"
        )

        print(
            "Memory: PERSISTENT"
        )

        print(
            "Tools:",
            ", ".join(
                krish.tools.list()
            ),
        )

        print(
            "=" * 70
        )

        krish.authenticate_owner()

        krish.grant_basic_permissions()

        krish.runtime.start()

        krish.chat()

    finally:

        krish.shutdown()


if __name__ == "__main__":

    main()