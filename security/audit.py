import hashlib
import json

from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass(frozen=True)
class AuditEntry:
    sequence: int
    action: str
    result: str
    timestamp: datetime
    details: dict
    previous_hash: str
    entry_hash: str


class AuditLog:
    """
    Tamper-evident in-memory security audit log.

    Every entry contains the hash of the previous
    entry, creating a hash chain.

    Any modification, deletion, reordering, or
    insertion into the chain causes integrity
    verification to fail.
    """

    GENESIS_HASH = "GENESIS"

    def __init__(self):
        self.entries: list[AuditEntry] = []

    @staticmethod
    def _validate_text(value, field_name):
        if not isinstance(value, str):
            raise TypeError(
                f"{field_name} must be a string."
            )

        value = value.strip()

        if not value:
            raise ValueError(
                f"{field_name} cannot be empty."
            )

        return value

    @staticmethod
    def _hash(
        sequence,
        action,
        result,
        timestamp,
        details,
        previous_hash,
    ):
        payload = {
            "sequence": sequence,
            "action": action,
            "result": result,
            "timestamp": timestamp.isoformat(),
            "details": details,
            "previous_hash": previous_hash,
        }

        data = json.dumps(
            payload,
            sort_keys=True,
            separators=(",", ":"),
            default=str,
        ).encode("utf-8")

        return hashlib.sha256(
            data
        ).hexdigest()

    def record(
        self,
        action,
        result,
        **details,
    ):
        action = self._validate_text(
            action,
            "Action",
        )

        result = self._validate_text(
            result,
            "Result",
        )

        timestamp = datetime.now(
            timezone.utc
        )

        sequence = len(self.entries) + 1

        previous_hash = (
            self.entries[-1].entry_hash
            if self.entries
            else self.GENESIS_HASH
        )

        safe_details = dict(details)

        entry_hash = self._hash(
            sequence=sequence,
            action=action,
            result=result,
            timestamp=timestamp,
            details=safe_details,
            previous_hash=previous_hash,
        )

        entry = AuditEntry(
            sequence=sequence,
            action=action,
            result=result,
            timestamp=timestamp,
            details=safe_details,
            previous_hash=previous_hash,
            entry_hash=entry_hash,
        )

        self.entries.append(entry)

        return entry

    def verify_integrity(self):
        """
        Verify the complete audit hash chain.
        """

        previous_hash = self.GENESIS_HASH

        for index, entry in enumerate(
            self.entries,
            start=1,
        ):
            if entry.sequence != index:
                return False

            if entry.previous_hash != previous_hash:
                return False

            expected_hash = self._hash(
                sequence=entry.sequence,
                action=entry.action,
                result=entry.result,
                timestamp=entry.timestamp,
                details=entry.details,
                previous_hash=entry.previous_hash,
            )

            if entry.entry_hash != expected_hash:
                return False

            previous_hash = entry.entry_hash

        return True

    def count(self):
        return len(self.entries)

    def latest(self):
        if not self.entries:
            return None

        return self.entries[-1]

    def status(self):
        return {
            "entries": len(self.entries),
            "integrity": self.verify_integrity(),
        }