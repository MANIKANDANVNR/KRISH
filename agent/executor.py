from security.risk import RiskLevel


class ApprovalRequired(Exception):

    def __init__(
        self,
        request_id,
        permission,
        reason,
    ):

        self.request_id = request_id
        self.permission = permission
        self.reason = reason

        super().__init__(
            f"Approval required: {permission}"
        )


class Executor:

    def __init__(
        self,
        tools=None,
        security=None,
    ):

        self.tools = tools
        self.security = security

    def _authorize(
        self,
        tool,
        session_id,
        risk=None,
        request_id=None,
        reason=None,
    ):

        if self.security is None:
            raise PermissionError(
                "Security gateway unavailable."
            )

        if session_id is None:
            raise PermissionError(
                "Owner session required."
            )

        actual_risk = risk

        if actual_risk is None:
            actual_risk = tool.risk

        if isinstance(actual_risk, str):

            actual_risk = RiskLevel[
                actual_risk.upper()
            ]

        requires_approval = (
            self.security.policy.requires_approval(
                actual_risk
            )
        )

        # ---------------------------------------------------------
        # HIGH / CRITICAL
        # ---------------------------------------------------------

        if (
            requires_approval
            and not request_id
        ):

            approval = (
                self.security.approvals.create(
                    permission=tool.permission,
                    reason=(
                        reason
                        or f"Execute {tool.name}"
                    ),
                    session_id=session_id,
                )
            )

            self.security.audit.record(
                "approval",
                "requested",
                permission=tool.permission,
                risk=actual_risk.name,
                request_id=approval.request_id,
            )

            raise ApprovalRequired(
                approval.request_id,
                tool.permission,
                approval.reason,
            )

        # ---------------------------------------------------------
        # SECURITY AUTHORIZATION
        # ---------------------------------------------------------

        allowed = self.security.authorize(
            tool.permission,
            risk=actual_risk,
            request_id=request_id,
            session_id=session_id,
        )

        if not allowed:

            raise PermissionError(
                f"Permission denied: "
                f"{tool.permission}"
            )

        # ---------------------------------------------------------
        # ONE-TIME APPROVAL CONSUMPTION
        # ---------------------------------------------------------

        if (
            requires_approval
            and request_id
        ):

            consumed = (
                self.security.approvals.consume(
                    request_id,
                    session_id,
                )
            )

            if not consumed:

                raise PermissionError(
                    "Approval could not be consumed."
                )

            self.security.audit.record(
                "approval",
                "consumed",
                permission=tool.permission,
                risk=actual_risk.name,
                request_id=request_id,
            )

    def execute(
        self,
        step,
        session_id=None,
        request_id=None,
    ):

        action = step.get("action")

        if action == "respond":

            return step.get(
                "input",
                "",
            )

        if action == "calculator":

            tool = self.tools.get(
                "calculator"
            )

            self._authorize(
                tool,
                session_id,
                request_id=request_id,
                reason=(
                    "Execute calculator "
                    "operation."
                ),
            )

            return tool.execute(
                step["input"]
            )

        if action == "file.read":

            tool = self.tools.get(
                "file"
            )

            self._authorize(
                tool,
                session_id,
                request_id=request_id,
                reason=(
                    "Read a file through "
                    "KRISH."
                ),
            )

            return tool.read(
                step["path"]
            )

        if action == "file.write":

            tool = self.tools.get(
                "file"
            )

            self._authorize(
                tool,
                session_id,
                request_id=request_id,
                reason=(
                    "Write data to a file "
                    "through KRISH."
                ),
            )

            return tool.write(
                step["path"],
                step["content"],
            )

        if action == "python":

            tool = self.tools.get(
                "python"
            )

            self._authorize(
                tool,
                session_id,
                request_id=request_id,
                reason=(
                    "Execute a Python expression "
                    "through KRISH."
                ),
            )

            return tool.execute(
                step["input"]
            )

        if action == "web.get":

            tool = self.tools.get(
                "web"
            )

            self._authorize(
                tool,
                session_id,
                request_id=request_id,
                reason=(
                    "Access an external web "
                    "resource."
                ),
            )

            return tool.get(
                step["url"]
            )

        if action == "system.open_calculator":

            tool = self.tools.get(
                "system"
            )

            self._authorize(
                tool,
                session_id,
                request_id=request_id,
                reason=(
                    "Open the Windows system "
                    "calculator application."
                ),
            )

            return tool.execute(
                "open_calculator"
            )

        raise ValueError(
            f"Unknown action: {action}"
        )