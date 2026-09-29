import secrets

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone


@dataclass
class Session:
    session_id: str
    owner_id: str
    created_at: datetime
    expires_at: datetime
    active: bool = True


class SessionManager:
    """
    Manages authenticated owner sessions.

    Sessions are:
    - random
    - time-limited
    - explicitly revocable
    - fail-closed after expiry
    """

    def __init__(self, lifetime_minutes=30):
        if lifetime_minutes <= 0:
            raise ValueError(
                "Session lifetime must be greater than zero."
            )

        self.lifetime_minutes = lifetime_minutes
        self._sessions = {}

    def create(self, owner_id):
        """
        Create a new owner session.

        Any caller that reaches this method is expected
        to have passed authentication at the SecurityKernel
        layer.
        """
        if owner_id is None:
            raise ValueError("Owner ID required.")

        owner_id = str(owner_id).strip()

        if not owner_id:
            raise ValueError("Owner ID required.")

        now = datetime.now(timezone.utc)

        session = Session(
            session_id=secrets.token_urlsafe(32),
            owner_id=owner_id,
            created_at=now,
            expires_at=(
                now
                + timedelta(
                    minutes=self.lifetime_minutes
                )
            ),
        )

        self._sessions[session.session_id] = session

        return session

    def get(self, session_id):
        """
        Return a session object or None.
        """
        if not session_id:
            return None

        return self._sessions.get(session_id)

    def validate(self, session_id):
        """
        Validate that a session exists, is active,
        and has not expired.
        """
        session = self.get(session_id)

        if session is None:
            return False

        if not session.active:
            return False

        if datetime.now(timezone.utc) >= session.expires_at:
            session.active = False
            return False

        return True

    def remaining_seconds(self, session_id):
        """
        Return remaining lifetime in seconds.

        Returns 0 for an invalid or expired session.
        """
        session = self.get(session_id)

        if session is None:
            return 0

        if not self.validate(session_id):
            return 0

        remaining = (
            session.expires_at
            - datetime.now(timezone.utc)
        ).total_seconds()

        return max(0, int(remaining))

    def revoke(self, session_id):
        """
        Revoke one session.
        """
        session = self.get(session_id)

        if session:
            session.active = False

    def revoke_all(self):
        """
        Revoke every active session.
        """
        for session in self._sessions.values():
            session.active = False

    def active_sessions(self):
        """
        Return currently valid sessions.
        """
        active = []

        for session in self._sessions.values():
            if self.validate(session.session_id):
                active.append(session)

        return tuple(active)

    def count_active(self):
        return len(self.active_sessions())

    def status(self):
        """
        Return safe session information.

        Session IDs are intentionally not returned here.
        """
        return {
            "lifetime_minutes": self.lifetime_minutes,
            "active_sessions": self.count_active(),
        }