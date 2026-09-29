class PermissionEngine:

    """
    Central permission store.

    This class only stores explicit permissions.

    It does NOT:
        - authenticate users
        - approve high-risk actions
        - enable capabilities
        - execute tools
        - bypass SecurityPolicy

    Those responsibilities belong to the higher-level
    security authorization/kernel layers.
    """

    def __init__(self):
        self._permissions = set()

    # =========================================================
    # PERMISSION NORMALIZATION
    # =========================================================

    @staticmethod
    def _normalize(permission):
        """
        Normalize a permission into a canonical form.
        """

        if not isinstance(permission, str):
            raise TypeError(
                "Permission must be a string."
            )

        permission = permission.strip().lower()

        if not permission:
            raise ValueError(
                "Permission cannot be empty."
            )

        return permission

    # =========================================================
    # GRANT
    # =========================================================

    def grant(self, permission):
        """
        Explicitly grant a permission.

        Granting a permission does not itself execute an
        operation or enable a runtime capability.
        """

        permission = self._normalize(permission)

        self._permissions.add(permission)

        return True

    # =========================================================
    # REVOKE
    # =========================================================

    def revoke(self, permission):
        """
        Revoke a permission.

        Revoking a permission is always safe.
        """

        permission = self._normalize(permission)

        self._permissions.discard(permission)

        return True

    # =========================================================
    # CHECK
    # =========================================================

    def allowed(self, permission):
        """
        Check whether a permission has been explicitly granted.
        """

        permission = self._normalize(permission)

        return permission in self._permissions

    def require(self, permission):
        """
        Require an explicitly granted permission.

        Raises PermissionError when unavailable.
        """

        permission = self._normalize(permission)

        if permission not in self._permissions:
            raise PermissionError(
                f"Permission denied: {permission}"
            )

        return True

    def contains(self, permission):
        """
        Compatibility alias for allowed().
        """

        return self.allowed(permission)

    # =========================================================
    # INFORMATION
    # =========================================================

    def list(self):
        """
        Return all currently granted permissions.
        """

        return tuple(
            sorted(self._permissions)
        )

    def count(self):
        """
        Return the number of granted permissions.
        """

        return len(self._permissions)

    def is_empty(self):
        """
        Return True when no permissions are granted.
        """

        return not self._permissions

    # =========================================================
    # CLEAR
    # =========================================================

    def clear(self):
        """
        Remove every granted permission.
        """

        self._permissions.clear()

        return True

    # =========================================================
    # STATUS
    # =========================================================

    def status(self):
        """
        Return a safe status snapshot for the security UI.
        """

        return {
            "count": len(self._permissions),
            "permissions": self.list(),
        }