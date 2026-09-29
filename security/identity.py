from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass(frozen=True)
class OwnerIdentity:

    owner_id: str
    display_name: str
    created_at: datetime

    @classmethod
    def create(
        cls,
        owner_id: str,
        display_name: str,
    ):

        owner_id = owner_id.strip()
        display_name = display_name.strip()

        if not owner_id:
            raise ValueError(
                "Owner ID cannot be empty."
            )

        if not display_name:
            raise ValueError(
                "Display name cannot be empty."
            )

        return cls(
            owner_id,
            display_name,
            datetime.now(timezone.utc),
        )