from dataclasses import dataclass

from security.risk import RiskLevel


@dataclass(frozen=True)
class SecurityPolicy:

    # =========================================================
    # CORE SECURITY
    # =========================================================

    # Everything is denied unless explicitly authorized.
    denied_by_default: bool = True

    # =========================================================
    # EVOLUTION / AUTHORITY
    # =========================================================

    # KRISH cannot modify its own security policy or core
    # behavior autonomously.
    self_modification: bool = False

    # KRISH cannot increase its own authority.
    authority_expansion: bool = False

    # KRISH cannot grant itself permissions.
    autonomous_permission_grant: bool = False

    # KRISH cannot autonomously deploy changes.
    autonomous_deployment: bool = False

    # =========================================================
    # APPROVAL POLICY
    # =========================================================

    high_risk_requires_approval: bool = True

    critical_requires_approval: bool = True

    # =========================================================
    # CAPABILITY SECURITY POLICY
    #
    # These values define the minimum risk level associated
    # with enabling each runtime capability.
    #
    # UI controls NEVER override these values.
    # =========================================================

    internet_risk: RiskLevel = RiskLevel.HIGH

    web_search_risk: RiskLevel = RiskLevel.MEDIUM

    external_data_risk: RiskLevel = RiskLevel.MEDIUM

    file_access_risk: RiskLevel = RiskLevel.HIGH

    system_access_risk: RiskLevel = RiskLevel.CRITICAL

    application_launch_risk: RiskLevel = RiskLevel.HIGH

    python_terminal_risk: RiskLevel = RiskLevel.CRITICAL

    voice_input_risk: RiskLevel = RiskLevel.LOW

    voice_output_risk: RiskLevel = RiskLevel.LOW

    # =========================================================
    # APPROVAL REQUIREMENTS
    # =========================================================

    def requires_approval(self, risk):
        """
        Determine whether a risk level requires explicit
        owner approval.

        Invalid risk values fail closed.
        """

        if not isinstance(risk, RiskLevel):
            try:
                risk = RiskLevel(risk)
            except (TypeError, ValueError):
                return True

        if risk == RiskLevel.CRITICAL:
            return self.critical_requires_approval

        if risk == RiskLevel.HIGH:
            return self.high_risk_requires_approval

        return False

    # =========================================================
    # CAPABILITY RISK LOOKUP
    # =========================================================

    def capability_risk(self, capability):
        """
        Return the security risk associated with a capability.

        Unknown capabilities are treated as CRITICAL so that a
        new capability cannot accidentally become low risk.
        """

        if not isinstance(capability, str):
            return RiskLevel.CRITICAL

        capability = capability.strip().lower()

        if not capability:
            return RiskLevel.CRITICAL

        risks = {
            "internet": self.internet_risk,
            "web_search": self.web_search_risk,
            "external_data": self.external_data_risk,
            "file_access": self.file_access_risk,
            "system_access": self.system_access_risk,
            "application_launch": self.application_launch_risk,
            "python_terminal": self.python_terminal_risk,
            "voice_input": self.voice_input_risk,
            "voice_output": self.voice_output_risk,
        }

        return risks.get(
            capability,
            RiskLevel.CRITICAL,
        )

    # =========================================================
    # KNOWN CAPABILITIES
    # =========================================================

    def capabilities(self):
        """
        Return the capabilities explicitly defined by policy.
        """

        return (
            "internet",
            "web_search",
            "external_data",
            "file_access",
            "system_access",
            "application_launch",
            "python_terminal",
            "voice_input",
            "voice_output",
        )

    # =========================================================
    # POLICY STATUS
    # =========================================================

    def status(self):
        """
        Return a safe, UI-friendly policy status snapshot.
        """

        return {
            "denied_by_default": self.denied_by_default,

            "self_modification": self.self_modification,

            "authority_expansion": (
                self.authority_expansion
            ),

            "autonomous_permission_grant": (
                self.autonomous_permission_grant
            ),

            "autonomous_deployment": (
                self.autonomous_deployment
            ),

            "high_risk_requires_approval": (
                self.high_risk_requires_approval
            ),

            "critical_requires_approval": (
                self.critical_requires_approval
            ),

            "capabilities": {
                capability: self.capability_risk(
                    capability
                ).name
                for capability in self.capabilities()
            },
        }