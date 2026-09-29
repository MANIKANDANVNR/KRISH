class HealthChecker:

    def check(
        self,
        runtime,
        security,
        brain=None,
    ):

        result = {
            "runtime":
                runtime.lifecycle.state.value,

            "security":
                security.active,

            "lockdown":
                security.lockdown.active,

            "audit":
                security.audit.verify_integrity(),
        }

        if brain:

            result["providers"] = (
                brain.router.health()
            )

        return result