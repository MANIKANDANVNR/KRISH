from enum import IntEnum


class RiskLevel(IntEnum):
    """
    Security risk classification.

    LOW:
        Normal low-risk operations.

    MEDIUM:
        Operations with limited external impact.

    HIGH:
        Operations requiring explicit owner approval.

    CRITICAL:
        Operations requiring explicit owner approval
        and the strongest security controls.
    """

    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


def normalize_risk(value):
    """
    Convert supported values into RiskLevel.

    Accepted:
        RiskLevel.LOW
        "low"
        "LOW"
        1

    Invalid values fail closed.
    """

    if isinstance(value, RiskLevel):
        return value

    if isinstance(value, bool):
        raise ValueError(
            f"Invalid risk: {value}"
        )

    if isinstance(value, str):
        value = value.strip()

        if not value:
            raise ValueError(
                "Risk cannot be empty."
            )

        try:
            return RiskLevel[
                value.upper()
            ]
        except KeyError as error:
            raise ValueError(
                f"Invalid risk: {value}"
            ) from error

    if isinstance(value, int):
        try:
            return RiskLevel(value)
        except ValueError as error:
            raise ValueError(
                f"Invalid risk: {value}"
            ) from error

    raise ValueError(
        f"Invalid risk: {value}"
    )


def requires_owner_approval(risk):
    """
    Return whether the supplied risk requires
    explicit owner approval.
    """

    risk = normalize_risk(risk)

    return risk in (
        RiskLevel.HIGH,
        RiskLevel.CRITICAL,
    )