class Recovery:

    def recover(
        self,
        error,
        step=None,
    ):

        return {
            "success": False,
            "error": str(error),
            "step": step,
        }