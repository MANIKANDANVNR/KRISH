class KrishError(Exception):
    pass


class SecurityError(KrishError):
    pass


class AuthorizationError(SecurityError):
    pass


class AuthenticationError(SecurityError):
    pass


class ToolError(KrishError):
    pass


class PlanningError(KrishError):
    pass


class VerificationError(KrishError):
    pass