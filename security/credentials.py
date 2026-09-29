import hashlib
import hmac
import os


class CredentialManager:

    def __init__(self, iterations=310_000):
        self.iterations = iterations

    def hash_secret(self, secret):

        if not isinstance(secret, str):
            raise TypeError(
                "Secret must be text."
            )

        if not secret:
            raise ValueError(
                "Secret cannot be empty."
            )

        salt = os.urandom(32)

        digest = hashlib.pbkdf2_hmac(
            "sha256",
            secret.encode(),
            salt,
            self.iterations,
        )

        return {
            "algorithm": "pbkdf2_sha256",
            "iterations": self.iterations,
            "salt": salt.hex(),
            "digest": digest.hex(),
        }

    def verify_secret(
        self,
        secret,
        record,
    ):

        try:

            salt = bytes.fromhex(
                record["salt"]
            )

            expected = bytes.fromhex(
                record["digest"]
            )

            actual = hashlib.pbkdf2_hmac(
                "sha256",
                secret.encode(),
                salt,
                int(record["iterations"]),
            )

            return hmac.compare_digest(
                actual,
                expected,
            )

        except (
            KeyError,
            ValueError,
            TypeError,
        ):
            return False