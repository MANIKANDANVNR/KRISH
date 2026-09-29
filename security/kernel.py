from datetime import datetime

from security.approval import ApprovalGate
from security.audit import AuditLog
from security.authentication import AuthenticationManager
from security.authorization import AuthorizationManager
from security.credentials import CredentialManager
from security.identity import OwnerIdentity
from security.lockdown import EmergencyLockdown
from security.permissions import PermissionEngine
from security.policy import SecurityPolicy
from security.risk import RiskLevel, normalize_risk
from security.session import SessionManager


class SecurityKernel:
    """
    Central security authority for KRISH.

    Security architecture:

        UI
         ↓
        SecurityKernel
         ↓
        Authentication
         ↓
        Owner Session
         ↓
        Authorization
         ↓
        Permission / Approval
         ↓
        Capability State
         ↓
        Tool Registry
         ↓
        Tool

    Security principles:

        • Deny by default
        • Fail closed
        • Authentication before authorization
        • Active owner session required
        • Owner UI authorization is required to activate capabilities
        • High/Critical capabilities require ApprovalGate approval
        • Approvals are single-use
        • Disabling never requires authorization
        • Lockdown invalidates authority
        • Startup never restores elevated capabilities
        • Session expiration disables capabilities
        • Automatic evolution is permanently OFF
        • KRISH cannot grant itself authority
        • The AI cannot authorize its own capability changes
    """

    # =========================================================
    # CAPABILITY DEFINITIONS
    # =========================================================

    CAPABILITIES = (
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
    # INITIALIZATION
    # =========================================================

    def __init__(
        self,
        session_minutes=30,
        repository=None,
    ):
        self.active = False

        self.owner = None
        self.repository = repository

        # -----------------------------------------------------
        # SECURITY COMPONENTS
        # -----------------------------------------------------

        self.policy = SecurityPolicy()

        self.credentials = CredentialManager()

        self.auth = AuthenticationManager(
            self.credentials
        )

        self.sessions = SessionManager(
            session_minutes
        )

        self.permissions = PermissionEngine()

        self.approvals = ApprovalGate()

        self.audit = AuditLog()

        self.lockdown = EmergencyLockdown()

        self.authorization = None

        # -----------------------------------------------------
        # ACTIVE OWNER SESSION
        # -----------------------------------------------------

        self.active_session = None
        self.active_session_id = None

        # -----------------------------------------------------
        # RUNTIME CAPABILITY STATE
        #
        # EVERYTHING STARTS OFF.
        # -----------------------------------------------------

        self._capabilities = {
            capability: False
            for capability in self.CAPABILITIES
        }

    # =========================================================
    # INITIALIZATION
    # =========================================================

    def initialize(self):
        """
        Initialize the security subsystem.

        Startup always begins with every capability disabled.

        Persisted capability state is deliberately ignored.
        """

        self.active = True

        self.authorization = AuthorizationManager(
            self.auth,
            self.permissions,
            self.approvals,
            self.sessions,
            self.lockdown,
            self.policy,
        )

        self._load_state()

        # -----------------------------------------------------
        # SECURITY RULE:
        # NEVER RESTORE CAPABILITIES FROM STORAGE
        # -----------------------------------------------------

        self._disable_all_capabilities()

        self.audit.record(
            "security",
            "initialized",
        )

        return True

    # =========================================================
    # PERSISTED STATE
    # =========================================================

    def _load_state(self):

        if not self.repository:
            return

        owner = self.repository.get_setting(
            "security.owner"
        )

        credential = self.repository.get_setting(
            "security.credential"
        )

        if owner:
            self.owner = OwnerIdentity(
                owner["owner_id"],
                owner["display_name"],
                datetime.fromisoformat(
                    owner["created_at"]
                ),
            )

        if credential:
            self.auth._record = credential

    def _save_owner(self):

        if (
            not self.repository
            or not self.owner
        ):
            return

        self.repository.set_setting(
            "security.owner",
            {
                "owner_id": self.owner.owner_id,
                "display_name": self.owner.display_name,
                "created_at": (
                    self.owner.created_at.isoformat()
                ),
            },
        )

    # =========================================================
    # OWNER
    # =========================================================

    def register_owner(
        self,
        owner_id,
        display_name,
    ):
        if not self.active:
            raise RuntimeError(
                "Security is inactive."
            )

        self.owner = OwnerIdentity.create(
            owner_id,
            display_name,
        )

        self._save_owner()

        self.audit.record(
            "owner",
            "registered",
        )

        return True

    # =========================================================
    # CREDENTIALS
    # =========================================================

    def configure_secret(
        self,
        secret,
    ):
        if self.owner is None:
            raise RuntimeError(
                "Register owner first."
            )

        self.auth.configure_secret(
            secret
        )

        if self.repository:
            self.repository.set_setting(
                "security.credential",
                self.auth._record,
            )

        self.audit.record(
            "credential",
            "configured",
        )

        return True

    def has_configured_secret(self):
        return bool(
            self.auth.configured
        )

    # =========================================================
    # AUTHENTICATION
    # =========================================================

    def authenticate(
        self,
        secret,
    ):
        if not self.active:
            return False

        if self.lockdown.active:
            self.audit.record(
                "authentication",
                "denied_lockdown",
            )
            return False

        result = self.auth.authenticate(
            secret
        )

        self.audit.record(
            "authentication",
            "success"
            if result
            else "denied",
        )

        return bool(result)

    @property
    def authenticated(self):
        return bool(
            self.auth.authenticated
        )

    @property
    def authentication(self):
        return self.auth

    # =========================================================
    # SESSION
    # =========================================================

    def create_session(self):
        """
        Create a new authenticated owner session.

        Only one active owner session exists at a time.
        """

        if not self.active:
            raise RuntimeError(
                "Security is inactive."
            )

        if self.lockdown.active:
            raise PermissionError(
                "Security lockdown is active."
            )

        if not self.auth.authenticated:
            raise PermissionError(
                "Authentication required."
            )

        if self.owner is None:
            raise RuntimeError(
                "Owner not configured."
            )

        if self.active_session_id is not None:
            try:
                self.sessions.revoke(
                    self.active_session_id
                )
            except Exception:
                pass

        session = self.sessions.create(
            self.owner.owner_id
        )

        self.active_session = session

        self.active_session_id = getattr(
            session,
            "session_id",
            session
            if isinstance(
                session,
                str,
            )
            else None,
        )

        if self.active_session_id is None:
            self.active_session = None

            raise RuntimeError(
                "Unable to establish security session."
            )

        self.audit.record(
            "session",
            "created",
        )

        return session

    @property
    def session(self):
        return self.sessions

    def get_active_session_id(self):
        """
        Return the currently valid owner session.

        Expired sessions immediately disable every capability.
        """

        if self.active_session_id is None:
            return None

        try:
            valid = self.sessions.validate(
                self.active_session_id
            )
        except Exception:
            valid = False

        if not valid:

            self.active_session = None
            self.active_session_id = None

            self._disable_all_capabilities()

            self.audit.record(
                "session",
                "expired",
            )

            return None

        return self.active_session_id

    def end_session(self):
        """
        End the current owner session.

        All capabilities and session approvals are revoked.
        """

        session_id = self.active_session_id

        if session_id is None:
            self._disable_all_capabilities()
            return True

        try:
            self.sessions.revoke(
                session_id
            )
        except Exception:
            pass

        try:
            self.approvals.revoke_session_requests(
                session_id
            )
        except Exception:
            pass

        self.active_session = None
        self.active_session_id = None

        self._disable_all_capabilities()

        self.audit.record(
            "session",
            "ended",
        )

        return True

    def logout(self):
        """
        Strong logout.

        Session, approvals and capabilities are invalidated.
        """

        self.end_session()

        self.auth.logout()

        self.audit.record(
            "authentication",
            "logout",
        )

        return True

    # =========================================================
    # AUTHORIZATION
    # =========================================================

    def authorize(
        self,
        permission,
        risk=RiskLevel.LOW,
        request_id=None,
        session_id=None,
    ):
        """
        Central authorization pipeline.

        This method NEVER enables a capability.
        """

        if not self.active:
            return False

        if self.lockdown.active:
            return False

        if self.authorization is None:
            return False

        if not self.auth.authenticated:
            return False

        session_id = (
            session_id
            or self.get_active_session_id()
        )

        if session_id is None:
            return False

        try:
            risk = normalize_risk(
                risk
            )
        except Exception:
            return False

        try:
            result = self.authorization.authorize(
                permission,
                risk,
                request_id,
                session_id,
            )

        except Exception as error:

            self.audit.record(
                "authorization",
                "denied",
                permission=permission,
                risk=risk.name,
                reason=str(error),
            )

            return False

        self.audit.record(
            "authorization",
            "allowed"
            if result
            else "denied",
            permission=permission,
            risk=risk.name,
        )

        return bool(result)

    # =========================================================
    # CAPABILITY NORMALIZATION
    # =========================================================

    def _normalize_capability(
        self,
        capability,
    ):
        if not isinstance(
            capability,
            str,
        ):
            raise TypeError(
                "Capability must be a string."
            )

        capability = capability.strip().lower()

        if capability not in self.CAPABILITIES:
            raise ValueError(
                f"Unknown capability: {capability}"
            )

        return capability

    # =========================================================
    # CAPABILITY PERMISSION
    # =========================================================

    @staticmethod
    def capability_permission(
        capability,
    ):
        if not isinstance(
            capability,
            str,
        ):
            raise TypeError(
                "Capability must be a string."
            )

        capability = capability.strip().lower()

        if not capability:
            raise ValueError(
                "Capability cannot be empty."
            )

        return (
            f"capability."
            f"{capability}"
            f".enable"
        )

    # =========================================================
    # CAPABILITY RISK
    # =========================================================

    def capability_risk(
        self,
        capability,
    ):
        """
        Public risk lookup for Settings/UI.

        This does not authorize anything.
        """

        capability = (
            self._normalize_capability(
                capability
            )
        )

        return self.policy.capability_risk(
            capability
        )

    # =========================================================
    # CAPABILITY STATE
    # =========================================================

    def capability_enabled(
        self,
        capability,
    ):
        capability = (
            self._normalize_capability(
                capability
            )
        )

        self.get_active_session_id()

        return bool(
            self._capabilities[
                capability
            ]
        )

    def capabilities(self):
        """
        Return a defensive capability snapshot.
        """

        self.get_active_session_id()

        return dict(
            self._capabilities
        )

    def capability_state(self):
        return self.capabilities()

    # =========================================================
    # OWNER CAPABILITY AUTHORIZATION
    # =========================================================

    def owner_authorize_capability(
        self,
        capability,
        session_id=None,
    ):
        """
        Authorize a capability from the authenticated owner
        control surface.

        This method is intentionally separate from the normal
        AI authorization pipeline.

        IMPORTANT:

            This is NOT an AI permission-granting mechanism.

        It requires:

            • Security active
            • No lockdown
            • Authenticated owner
            • Valid owner session
            • Known capability

        For LOW/MEDIUM capabilities:

            The owner explicitly authorizes the capability
            permission.

        For HIGH/CRITICAL capabilities:

            An ApprovalGate request is created, approved by
            the authenticated owner session, and then consumed
            by enable_capability().

        This method should only be called by the trusted UI /
        owner control layer and must never be exposed as an AI
        tool.
        """

        capability = (
            self._normalize_capability(
                capability
            )
        )

        if not self.active:
            raise RuntimeError(
                "Security is inactive."
            )

        if self.lockdown.active:
            raise PermissionError(
                "Security lockdown is active."
            )

        if not self.auth.authenticated:
            raise PermissionError(
                "Authentication required."
            )

        session_id = (
            session_id
            or self.get_active_session_id()
        )

        if session_id is None:
            raise PermissionError(
                "Active owner session required."
            )

        try:
            valid_session = self.sessions.validate(
                session_id
            )
        except Exception:
            valid_session = False

        if not valid_session:
            self._disable_all_capabilities()

            raise PermissionError(
                "Owner session is invalid or expired."
            )

        risk = self.policy.capability_risk(
            capability
        )

        permission = (
            self.capability_permission(
                capability
            )
        )

        # -----------------------------------------------------
        # HIGH / CRITICAL
        # -----------------------------------------------------

        if self.policy.requires_approval(
            risk
        ):

            request = self.approvals.create(
                permission=permission,
                reason=(
                    f"Owner requested activation of "
                    f"capability '{capability}'."
                ),
                session_id=session_id,
            )

            self.approvals.approve(
                request.request_id,
                session_id,
            )

            self.audit.record(
                "capability",
                "owner_approval_created",
                capability=capability,
                risk=risk.name,
            )

            return self.enable_capability(
                capability,
                request_id=request.request_id,
                session_id=session_id,
            )

        # -----------------------------------------------------
        # LOW / MEDIUM
        #
        # Explicit owner action establishes the capability
        # permission.
        # -----------------------------------------------------

        try:
            self.permissions.grant(
                permission
            )

        except Exception as error:

            self.audit.record(
                "capability",
                "owner_authorization_failed",
                capability=capability,
                risk=risk.name,
                reason=str(error),
            )

            raise PermissionError(
                "Unable to establish capability permission."
            ) from error

        self.audit.record(
            "capability",
            "owner_authorized",
            capability=capability,
            risk=risk.name,
        )

        try:
            return self.enable_capability(
                capability,
                session_id=session_id,
            )

        except Exception:
            # Do not leave an unused capability permission
            # behind when activation fails.
            try:
                self.permissions.revoke(
                    permission
                )
            except Exception:
                pass

            raise

    # =========================================================
    # ENABLE CAPABILITY
    # =========================================================

    def enable_capability(
        self,
        capability,
        request_id=None,
        session_id=None,
    ):
        """
        Enable a protected runtime capability.

        IMPORTANT:

        Normal AI/tool callers must already possess the
        required capability permission.

        Owner UI activation should use:

            owner_authorize_capability()

        HIGH/CRITICAL capabilities require ApprovalGate.
        """

        capability = (
            self._normalize_capability(
                capability
            )
        )

        if not self.active:
            raise RuntimeError(
                "Security is inactive."
            )

        if self.lockdown.active:
            raise PermissionError(
                "Security lockdown is active."
            )

        if not self.auth.authenticated:
            raise PermissionError(
                "Authentication required."
            )

        session_id = (
            session_id
            or self.get_active_session_id()
        )

        if session_id is None:
            raise PermissionError(
                "Active owner session required."
            )

        try:
            valid_session = self.sessions.validate(
                session_id
            )
        except Exception:
            valid_session = False

        if not valid_session:

            self.active_session = None
            self.active_session_id = None

            self._disable_all_capabilities()

            raise PermissionError(
                "Owner session is invalid or expired."
            )

        # -----------------------------------------------------
        # POLICY
        # -----------------------------------------------------

        risk = self.policy.capability_risk(
            capability
        )

        permission = (
            self.capability_permission(
                capability
            )
        )

        # -----------------------------------------------------
        # AUTHORIZATION
        # -----------------------------------------------------

        allowed = self.authorize(
            permission,
            risk,
            request_id=request_id,
            session_id=session_id,
        )

        if not allowed:

            self.audit.record(
                "capability",
                "enable_denied",
                capability=capability,
                risk=risk.name,
            )

            raise PermissionError(
                f"Capability authorization denied: "
                f"{capability}"
            )

        # -----------------------------------------------------
        # HIGH / CRITICAL APPROVAL
        # -----------------------------------------------------

        if self.policy.requires_approval(
            risk
        ):

            if not request_id:
                self.audit.record(
                    "capability",
                    "enable_denied",
                    capability=capability,
                    risk=risk.name,
                    reason="missing_approval_request",
                )

                raise PermissionError(
                    "Approval request required."
                )

            consume = getattr(
                self.authorization,
                "consume_approval",
                None,
            )

            if not callable(consume):
                raise PermissionError(
                    "Approval subsystem is unavailable."
                )

            try:
                consumed = consume(
                    request_id,
                    session_id,
                )

            except Exception as error:

                self.audit.record(
                    "capability",
                    "enable_denied",
                    capability=capability,
                    risk=risk.name,
                    reason="approval_consumption_failed",
                )

                raise PermissionError(
                    "Approval could not be consumed."
                ) from error

            if not consumed:

                raise PermissionError(
                    "Approval could not be consumed."
                )

        # -----------------------------------------------------
        # ENABLE
        # -----------------------------------------------------

        self._capabilities[
            capability
        ] = True

        self.audit.record(
            "capability",
            "enabled",
            capability=capability,
            risk=risk.name,
        )

        return True

    # =========================================================
    # DISABLE CAPABILITY
    # =========================================================

    def disable_capability(
        self,
        capability,
    ):
        """
        Disable a capability.

        Disabling never requires authentication or approval.
        """

        capability = (
            self._normalize_capability(
                capability
            )
        )

        was_enabled = bool(
            self._capabilities[
                capability
            ]
        )

        self._capabilities[
            capability
        ] = False

        if was_enabled:
            self.audit.record(
                "capability",
                "disabled",
                capability=capability,
            )

        return True

    # =========================================================
    # SET CAPABILITY
    # =========================================================

    def set_capability(
        self,
        capability,
        enabled,
        request_id=None,
        session_id=None,
    ):
        """
        Unified capability interface.

        OFF:
            Always allowed.

        ON:
            Must pass the security pipeline.
        """

        capability = (
            self._normalize_capability(
                capability
            )
        )

        if not bool(enabled):
            return self.disable_capability(
                capability
            )

        return self.enable_capability(
            capability,
            request_id=request_id,
            session_id=session_id,
        )

    # =========================================================
    # REQUIRE CAPABILITY
    # =========================================================

    def require_capability(
        self,
        capability,
    ):
        """
        Require a capability to be authenticated,
        session-valid and enabled.
        """

        capability = (
            self._normalize_capability(
                capability
            )
        )

        if not self.active:
            raise PermissionError(
                "Security is inactive."
            )

        if self.lockdown.active:
            raise PermissionError(
                "Security lockdown is active."
            )

        if not self.auth.authenticated:
            raise PermissionError(
                "Authentication required."
            )

        if self.get_active_session_id() is None:
            raise PermissionError(
                "Active owner session required."
            )

        if not self._capabilities[
            capability
        ]:
            raise PermissionError(
                f"Capability is disabled: "
                f"{capability}"
            )

        return True

    # =========================================================
    # CAPABILITY CHECK
    # =========================================================

    def is_capability_available(
        self,
        capability,
    ):
        capability = (
            self._normalize_capability(
                capability
            )
        )

        try:
            self.require_capability(
                capability
            )
            return True

        except Exception:
            return False

    # =========================================================
    # INTERNAL RESET
    # =========================================================

    def _disable_all_capabilities(self):

        for capability in self.CAPABILITIES:
            self._capabilities[
                capability
            ] = False

    # =========================================================
    # PUBLIC RESET
    # =========================================================

    def reset_capabilities(self):

        self._disable_all_capabilities()

        self.audit.record(
            "capability",
            "all_disabled",
        )

        return True

    def _reset_capabilities(self):
        return self.reset_capabilities()

    # =========================================================
    # AUTOMATIC EVOLUTION
    # =========================================================

    @property
    def automatic_evolution_enabled(self):
        """
        Automatic evolution is intentionally impossible.

        KRISH may only perform a specific improvement after
        explicit owner authorization through the evolution
        subsystem.

        This property always returns False.
        """

        return False

    def enable_automatic_evolution(self):
        """
        Deliberately rejected.

        Automatic evolution must never be enabled globally.
        """

        self.audit.record(
            "evolution",
            "denied",
            reason="automatic_evolution_disabled_by_policy",
        )

        raise PermissionError(
            "Automatic evolution is permanently disabled."
        )

    def disable_automatic_evolution(self):
        """
        Safe no-op.

        Automatic evolution is already disabled.
        """

        self.audit.record(
            "evolution",
            "disabled",
        )

        return True

    # =========================================================
    # SECURITY STATUS
    # =========================================================

    def status(self):
        """
        Return a complete safe security snapshot.

        Secrets and credential hashes are never exposed.
        """

        session_id = (
            self.get_active_session_id()
        )

        authentication = bool(
            self.auth.authenticated
        )

        authorization_active = (
            self.authorization is not None
        )

        return {
            "active": bool(
                self.active
            ),

            "authentication": authentication,

            "authenticated": authentication,

            "authorization": (
                authorization_active
            ),

            "permissions": (
                self.permissions.list()
            ),

            "permission_count": (
                self.permissions.count()
            ),

            "session": (
                session_id is not None
            ),

            "session_id": session_id,

            "lockdown": bool(
                self.lockdown.active
            ),

            "capabilities": self.capabilities(),

            "automatic_evolution": False,

            "owner_authorization_required": True,

            "policy": self.policy.status(),
        }

    # =========================================================
    # LOCKDOWN
    # =========================================================

    def lockdown_system(
        self,
        reason,
    ):
        """
        Immediately invalidate all authority.
        """

        self.lockdown.engage(
            reason
        )

        self.sessions.revoke_all()

        try:
            self.approvals.revoke_all()
        except Exception:
            pass

        self.active_session = None
        self.active_session_id = None

        self._disable_all_capabilities()

        self.auth.logout()

        self.audit.record(
            "lockdown",
            "engaged",
            reason=reason,
        )

        return True

    def release_lockdown(self):
        """
        Release lockdown without restoring authority.

        Owner must authenticate again and create a new session.
        """

        self.lockdown.release()

        self.active_session = None
        self.active_session_id = None

        self._disable_all_capabilities()

        self.auth.logout()

        self.audit.record(
            "lockdown",
            "released",
        )

        return True