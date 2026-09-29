from security.risk import RiskLevel


class AuthorizationManager:
    """
    Central authorization decision engine for KRISH.

    Authorization flow:

        Lockdown
            ↓
        Authentication
            ↓
        Valid Session
            ↓
        Risk Evaluation
            ↓
        Approval OR Permission
            ↓
        ALLOW / DENY

    This class makes authorization decisions only.

    It does NOT:

        • enable capabilities
        • execute tools
        • modify runtime capability state
        • create authentication sessions
        • create approval requests
        • grant permissions
        • change security policy

    The SecurityKernel remains the central security authority.
    """

    def __init__(
        self,
        authentication,
        permissions,
        approvals,
        sessions,
        lockdown,
        policy,
    ):
        self.authentication = authentication
        self.permissions = permissions
        self.approvals = approvals
        self.sessions = sessions
        self.lockdown = lockdown
        self.policy = policy

    # =========================================================
    # NORMALIZATION
    # =========================================================

    @staticmethod
    def _normalize_permission(permission):
        """
        Normalize a permission into a safe canonical form.

        Invalid permissions fail closed.
        """

        if not isinstance(
            permission,
            str,
        ):
            return None

        permission = permission.strip().lower()

        if not permission:
            return None

        return permission

    @staticmethod
    def _normalize_risk(risk):
        """
        Normalize a RiskLevel value.

        Invalid values return None instead of guessing.
        """

        if isinstance(
            risk,
            RiskLevel,
        ):
            return risk

        try:
            return RiskLevel(risk)
        except (
            TypeError,
            ValueError,
        ):
            return None

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
        Determine whether an operation is authorized.

        Returns:
            bool

        Security rules:

            • Invalid input → DENY
            • Lockdown → DENY
            • Unauthenticated → DENY
            • Missing session → DENY
            • Invalid session → DENY
            • Invalid risk → DENY
            • HIGH/CRITICAL → approval required
            • LOW/MEDIUM → explicit permission required

        Important:

            Successful authorization does NOT consume an
            approval request.

            Approval consumption is performed explicitly by
            consume_approval() after the protected state change
            succeeds.
        """

        # -----------------------------------------------------
        # PERMISSION
        # -----------------------------------------------------

        permission = (
            self._normalize_permission(
                permission
            )
        )

        if permission is None:
            return False

        # -----------------------------------------------------
        # LOCKDOWN
        # -----------------------------------------------------

        try:
            if self.lockdown.active:
                return False
        except Exception:
            # If lockdown state cannot be determined,
            # fail closed.
            return False

        # -----------------------------------------------------
        # AUTHENTICATION
        # -----------------------------------------------------

        try:
            if not self.authentication.authenticated:
                return False
        except Exception:
            return False

        # -----------------------------------------------------
        # SESSION
        # -----------------------------------------------------

        if not isinstance(
            session_id,
            str,
        ):
            return False

        session_id = session_id.strip()

        if not session_id:
            return False

        try:
            valid_session = self.sessions.validate(
                session_id
            )
        except Exception:
            valid_session = False

        if not valid_session:
            return False

        # -----------------------------------------------------
        # RISK
        # -----------------------------------------------------

        risk = self._normalize_risk(
            risk
        )

        if risk is None:
            return False

        # -----------------------------------------------------
        # APPROVAL POLICY
        # -----------------------------------------------------

        try:
            requires_approval = (
                self.policy.requires_approval(
                    risk
                )
            )
        except Exception:
            # If policy evaluation fails, do not guess.
            return False

        # -----------------------------------------------------
        # HIGH / CRITICAL
        # -----------------------------------------------------

        if requires_approval:

            return self._authorize_approved_operation(
                permission,
                request_id,
                session_id,
            )

        # -----------------------------------------------------
        # LOW / MEDIUM
        # -----------------------------------------------------

        return self._authorize_permission(
            permission
        )

    # =========================================================
    # APPROVAL-BASED AUTHORIZATION
    # =========================================================

    def _authorize_approved_operation(
        self,
        permission,
        request_id,
        session_id,
    ):
        """
        Authorize a HIGH or CRITICAL operation.

        Required:

            • request_id exists
            • approval exists
            • approval belongs to session
            • approval is still valid
            • approval has been approved
            • permission matches exactly

        The approval is NOT consumed here.
        """

        if not isinstance(
            request_id,
            str,
        ):
            return False

        request_id = request_id.strip()

        if not request_id:
            return False

        if not isinstance(
            session_id,
            str,
        ):
            return False

        session_id = session_id.strip()

        if not session_id:
            return False

        # -----------------------------------------------------
        # APPROVAL STATUS
        # -----------------------------------------------------

        try:
            approved = self.approvals.approved(
                request_id,
                session_id,
            )
        except Exception:
            return False

        if not approved:
            return False

        # -----------------------------------------------------
        # APPROVAL REQUEST
        # -----------------------------------------------------

        try:
            request = self.approvals.get(
                request_id
            )
        except Exception:
            return False

        if request is None:
            return False

        # -----------------------------------------------------
        # PERMISSION MATCH
        # -----------------------------------------------------

        request_permission = getattr(
            request,
            "permission",
            None,
        )

        request_permission = (
            self._normalize_permission(
                request_permission
            )
        )

        if request_permission is None:
            return False

        if request_permission != permission:
            return False

        # -----------------------------------------------------
        # SESSION OWNERSHIP
        # -----------------------------------------------------

        request_session = getattr(
            request,
            "session_id",
            None,
        )

        if request_session is not None:

            if request_session != session_id:
                return False

        return True

    # =========================================================
    # PERMISSION-BASED AUTHORIZATION
    # =========================================================

    def _authorize_permission(
        self,
        permission,
    ):
        """
        Authorize LOW/MEDIUM operations through the explicit
        permission store.

        Permission grants do not bypass authentication or
        session validation because those checks have already
        occurred in authorize().
        """

        try:
            return bool(
                self.permissions.allowed(
                    permission
                )
            )
        except Exception:
            return False

    # =========================================================
    # EXPLICIT APPROVAL CONSUMPTION
    # =========================================================

    def consume_approval(
        self,
        request_id,
        session_id,
    ):
        """
        Consume an already-approved request.

        This operation is intentionally separate from
        authorize().

        Correct sequence:

            authorize()
                ↓
            protected state change
                ↓
            consume_approval()

        This prevents an approval from being consumed before
        the protected operation actually succeeds.

        Approval consumption always fails closed.
        """

        if not isinstance(
            request_id,
            str,
        ):
            return False

        request_id = request_id.strip()

        if not request_id:
            return False

        if not isinstance(
            session_id,
            str,
        ):
            return False

        session_id = session_id.strip()

        if not session_id:
            return False

        # -----------------------------------------------------
        # LOCKDOWN
        # -----------------------------------------------------

        try:
            if self.lockdown.active:
                return False
        except Exception:
            return False

        # -----------------------------------------------------
        # AUTHENTICATION
        # -----------------------------------------------------

        try:
            if not self.authentication.authenticated:
                return False
        except Exception:
            return False

        # -----------------------------------------------------
        # SESSION
        # -----------------------------------------------------

        try:
            if not self.sessions.validate(
                session_id
            ):
                return False
        except Exception:
            return False

        # -----------------------------------------------------
        # APPROVAL
        # -----------------------------------------------------

        try:
            return bool(
                self.approvals.consume(
                    request_id,
                    session_id,
                )
            )
        except Exception:
            return False

    # =========================================================
    # APPROVAL INSPECTION
    # =========================================================

    def get_approval(
        self,
        request_id,
    ):
        """
        Return an approval request for controlled inspection.

        The returned object must not be treated as authorization
        by itself. Authorization must still pass through
        authorize().
        """

        if not isinstance(
            request_id,
            str,
        ):
            return None

        request_id = request_id.strip()

        if not request_id:
            return None

        try:
            return self.approvals.get(
                request_id
            )
        except Exception:
            return None

    def pending_approvals(self):
        """
        Return currently pending approval requests.

        Intended primarily for the Security UI.
        """

        try:
            return tuple(
                self.approvals.pending()
            )
        except Exception:
            return tuple()

    # =========================================================
    # PERMISSION INSPECTION
    # =========================================================

    def permissions_list(self):
        """
        Return currently granted permissions.

        Intended for security status displays.
        """

        try:
            return tuple(
                self.permissions.list()
            )
        except Exception:
            return tuple()

    # =========================================================
    # SECURITY STATUS
    # =========================================================

    def status(self):
        """
        Return a safe authorization status snapshot.

        No credentials, secrets or approval internals are
        exposed.
        """

        try:
            authenticated = bool(
                self.authentication.authenticated
            )
        except Exception:
            authenticated = False

        try:
            permissions = tuple(
                self.permissions.list()
            )
        except Exception:
            permissions = tuple()

        try:
            lockdown = bool(
                self.lockdown.active
            )
        except Exception:
            # Security status cannot be trusted if lockdown
            # cannot be determined.
            lockdown = True

        try:
            pending = len(
                self.approvals.pending()
            )
        except Exception:
            pending = 0

        return {
            "authentication": authenticated,

            "authorization": True,

            "permissions": permissions,

            "permission_count": len(
                permissions
            ),

            "lockdown": lockdown,

            "pending_approvals": pending,
        }