import secrets

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone


@dataclass
class ApprovalRequest:
    request_id: str
    permission: str
    reason: str
    session_id: str | None
    created_at: datetime
    expires_at: datetime
    approved: bool = False
    consumed: bool = False
    revoked: bool = False


class ApprovalGate:
    """
    Explicit owner approval gate for elevated operations.

    Security rules:
    - Every approval has a unique unpredictable ID.
    - Approvals are time limited.
    - Approvals can be bound to a session.
    - Approvals are single use.
    - Revoked or consumed approvals cannot be reused.
    - Expired approvals automatically become revoked.
    """

    DEFAULT_TTL_SECONDS = 60
    MAX_TTL_SECONDS = 300

    def __init__(self):
        self._requests: dict[str, ApprovalRequest] = {}

    @staticmethod
    def _validate_text(value, field_name):
        if not isinstance(value, str):
            raise TypeError(f"{field_name} must be a string.")

        value = value.strip()

        if not value:
            raise ValueError(f"{field_name} required.")

        return value

    @staticmethod
    def _validate_session_id(session_id):
        if session_id is None:
            return None

        if not isinstance(session_id, str):
            raise TypeError("Session ID must be a string.")

        session_id = session_id.strip()

        if not session_id:
            raise ValueError("Session ID cannot be empty.")

        return session_id

    def create(
        self,
        permission,
        reason,
        session_id=None,
        ttl_seconds=None,
    ):
        permission = self._validate_text(
            permission,
            "Permission",
        )

        reason = self._validate_text(
            reason,
            "Reason",
        )

        session_id = self._validate_session_id(
            session_id
        )

        if ttl_seconds is None:
            ttl = self.DEFAULT_TTL_SECONDS
        else:
            if isinstance(ttl_seconds, bool):
                raise TypeError(
                    "Approval TTL must be an integer."
                )

            if not isinstance(
                ttl_seconds,
                (int, float),
            ):
                raise TypeError(
                    "Approval TTL must be numeric."
                )

            if ttl_seconds <= 0:
                raise ValueError(
                    "Approval TTL must be greater than zero."
                )

            if ttl_seconds > self.MAX_TTL_SECONDS:
                raise ValueError(
                    f"Approval TTL cannot exceed "
                    f"{self.MAX_TTL_SECONDS} seconds."
                )

            ttl = ttl_seconds

        now = datetime.now(timezone.utc)

        request = ApprovalRequest(
            request_id=secrets.token_urlsafe(32),
            permission=permission,
            reason=reason,
            session_id=session_id,
            created_at=now,
            expires_at=(
                now + timedelta(seconds=ttl)
            ),
        )

        self._requests[request.request_id] = request

        return request

    def _get_valid_request(
        self,
        request_id,
        session_id=None,
    ):
        if not isinstance(request_id, str):
            raise TypeError(
                "Approval ID must be a string."
            )

        request_id = request_id.strip()

        if not request_id:
            raise ValueError(
                "Approval ID required."
            )

        session_id = self._validate_session_id(
            session_id
        )

        request = self._requests.get(request_id)

        if request is None:
            raise KeyError(
                "Unknown approval."
            )

        if request.revoked:
            raise RuntimeError(
                "Approval revoked."
            )

        if request.consumed:
            raise RuntimeError(
                "Approval already consumed."
            )

        now = datetime.now(timezone.utc)

        if now >= request.expires_at:
            request.revoked = True
            request.approved = False

            raise RuntimeError(
                "Approval expired."
            )

        if (
            request.session_id is not None
            and session_id != request.session_id
        ):
            raise PermissionError(
                "Approval belongs to another session."
            )

        return request

    def approve(
        self,
        request_id,
        session_id=None,
    ):
        request = self._get_valid_request(
            request_id,
            session_id,
        )

        request.approved = True

        return True

    def revoke(
        self,
        request_id,
        session_id=None,
    ):
        if not isinstance(request_id, str):
            raise TypeError(
                "Approval ID must be a string."
            )

        request = self._requests.get(
            request_id.strip()
        )

        if request is None:
            return False

        session_id = self._validate_session_id(
            session_id
        )

        if (
            request.session_id is not None
            and session_id != request.session_id
        ):
            raise PermissionError(
                "Approval belongs to another session."
            )

        request.approved = False
        request.revoked = True

        return True

    def approved(
        self,
        request_id,
        session_id=None,
    ):
        try:
            request = self._get_valid_request(
                request_id,
                session_id,
            )
        except (
            KeyError,
            RuntimeError,
            PermissionError,
            TypeError,
            ValueError,
        ):
            return False

        return bool(request.approved)

    def consume(
        self,
        request_id,
        session_id=None,
    ):
        request = self._get_valid_request(
            request_id,
            session_id,
        )

        if not request.approved:
            return False

        request.consumed = True
        request.approved = False

        return True

    def get(self, request_id):
        if not isinstance(request_id, str):
            return None

        return self._requests.get(
            request_id.strip()
        )

    def pending(self):
        """
        Return all currently valid approval requests.
        """

        now = datetime.now(timezone.utc)
        requests = []

        for request in self._requests.values():

            if request.revoked:
                continue

            if request.consumed:
                continue

            if now >= request.expires_at:
                request.revoked = True
                request.approved = False
                continue

            requests.append(request)

        return tuple(requests)

    def revoke_session_requests(
        self,
        session_id,
    ):
        if session_id is None:
            return 0

        session_id = self._validate_session_id(
            session_id
        )

        count = 0

        for request in self._requests.values():

            if (
                request.session_id == session_id
                and not request.consumed
                and not request.revoked
            ):
                request.approved = False
                request.revoked = True
                count += 1

        return count

    def revoke_all(self):
        count = 0

        for request in self._requests.values():

            if (
                not request.consumed
                and not request.revoked
            ):
                request.approved = False
                request.revoked = True
                count += 1

        return count

    def status(self):
        pending = self.pending()

        return {
            "pending": len(pending),
            "approved": sum(
                1
                for request in pending
                if request.approved
            ),
            "total": len(self._requests),
        }