class AuthenticationManager:
    """
    Handles owner authentication state.

    Responsibilities:
    - Store only the hashed owner secret.
    - Verify supplied secrets.
    - Track authentication state.
    - Never expose the original secret.
    """

    def __init__(self, credentials):
        self.credentials = credentials
        self._record = None
        self._authenticated = False

    def configure_secret(self, secret):
        """
        Configure or replace the owner secret.

        Changing the secret immediately invalidates
        the current authentication state.
        """
        if secret is None:
            raise ValueError("Secret required.")

        if not isinstance(secret, str):
            raise TypeError("Secret must be a string.")

        if not secret.strip():
            raise ValueError("Secret required.")

        self._record = self.credentials.hash_secret(secret)
        self._authenticated = False

    def authenticate(self, secret):
        """
        Authenticate using the configured owner secret.

        Returns:
            bool: True when authentication succeeds.
        """
        if self._record is None:
            self._authenticated = False
            return False

        if secret is None:
            self._authenticated = False
            return False

        if not isinstance(secret, str):
            self._authenticated = False
            return False

        try:
            self._authenticated = bool(
                self.credentials.verify_secret(
                    secret,
                    self._record,
                )
            )
        except Exception:
            # Authentication failures must fail closed.
            self._authenticated = False
            return False

        return self._authenticated

    def logout(self):
        """
        End the current authentication state.
        """
        self._authenticated = False

    def reset(self):
        """
        Clear authentication state and stored credentials.

        Intended for controlled security reset operations.
        """
        self._authenticated = False
        self._record = None

    @property
    def authenticated(self):
        return self._authenticated

    @property
    def configured(self):
        return self._record is not None

    def status(self):
        """
        Return safe authentication status.

        Never exposes the credential hash.
        """
        return {
            "configured": self.configured,
            "authenticated": self.authenticated,
        }