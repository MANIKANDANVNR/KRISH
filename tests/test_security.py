from security.kernel import SecurityKernel
from security.risk import RiskLevel


def build():

    security = SecurityKernel()

    security.initialize()

    security.register_owner(
        "OWNER",
        "Owner",
    )

    security.configure_secret(
        "test-secret"
    )

    return security


def test_authentication():

    security = build()

    assert security.authenticate(
        "test-secret"
    )

    assert security.auth.authenticated


def test_bad_authentication():

    security = build()

    assert not security.authenticate(
        "wrong-secret"
    )


def test_session():

    security = build()

    security.authenticate(
        "test-secret"
    )

    session = security.create_session()

    assert security.sessions.validate(
        session.session_id
    )


def test_permission():

    security = build()

    security.authenticate(
        "test-secret"
    )

    session = security.create_session()

    security.permissions.grant(
        "tool.calculator"
    )

    assert security.authorize(
        "tool.calculator",
        session_id=session.session_id,
    )


def test_denied_permission():

    security = build()

    security.authenticate(
        "test-secret"
    )

    session = security.create_session()

    assert not security.authorize(
        "tool.file",
        session_id=session.session_id,
    )


def test_high_risk_requires_approval():

    security = build()

    security.authenticate(
        "test-secret"
    )

    session = security.create_session()

    security.permissions.grant(
        "tool.python"
    )

    assert not security.authorize(
        "tool.python",
        RiskLevel.HIGH,
        session_id=session.session_id,
    )

    request = security.approvals.create(
        "tool.python",
        "Owner requested calculation.",
    )

    security.approvals.approve(
        request.request_id
    )

    assert security.authorize(
        "tool.python",
        RiskLevel.HIGH,
        request.request_id,
        session.session_id,
    )


def test_lockdown():

    security = build()

    security.authenticate(
        "test-secret"
    )

    session = security.create_session()

    security.permissions.grant(
        "tool.calculator"
    )

    security.lockdown_system(
        "Emergency test."
    )

    assert not security.authorize(
        "tool.calculator",
        session_id=session.session_id,
    )


def test_audit_integrity():

    security = build()

    security.authenticate(
        "test-secret"
    )

    assert security.audit.verify_integrity()