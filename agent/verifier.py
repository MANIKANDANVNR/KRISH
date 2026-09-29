class Verifier:

    def verify(self, result):

        if result is None:
            return False

        if isinstance(result, str):
            return bool(result.strip())

        return True