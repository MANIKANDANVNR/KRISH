from datetime import datetime, timezone


class EmergencyLockdown:
    """
    Emergency security lockdown.

    When active, higher security layers must reject
    protected operations.

    This class intentionally does not restore anything
    when lockdown is released. The SecurityKernel is
    responsible for restoring state explicitly.
    """

    def __init__(self):
        self.active = False
        self.reason = None
        self.activated_at = None

    def engage(self, reason):
        if not isinstance(reason, str):
            raise TypeError(
                "Lockdown reason must be a string."
            )

        if not reason.strip():
            raise ValueError(
                "Lockdown reason required."
            )

        self.active = True
        self.reason = reason.strip()
        self.activated_at = datetime.now(timezone.utc)

    def release(self):
        self.active = False
        self.reason = None
        self.activated_at = None

    def status(self):
        """
        Return safe lockdown state.
        """
        return {
            "active": self.active,
            "reason": self.reason,
            "activated_at": self.activated_at,
        }