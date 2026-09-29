class Reporter:

    def success(self, result):

        return {
            "success": True,
            "result": result,
        }

    def failure(self, error):

        return {
            "success": False,
            "error": str(error),
        }