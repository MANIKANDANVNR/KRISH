import platform
import subprocess


class SystemTool:

    name = "system"

    permission = "tool.system"

    risk = "high"

    ALLOWED = {
        "python_version": [
            "python",
            "--version",
        ],

        "system_info": [
            "systeminfo",
        ],

        "open_calculator": [
            "calc.exe",
        ],
    }

    def execute(
        self,
        action,
    ):

        if action not in self.ALLOWED:
            raise PermissionError(
                "System action is not allowed."
            )

        if action == "open_calculator":

            subprocess.Popen(
                self.ALLOWED[action],
                shell=False,
            )

            return {
                "success": True,
                "action": action,
            }

        result = subprocess.run(
            self.ALLOWED[action],
            capture_output=True,
            text=True,
            timeout=10,
            shell=False,
        )

        return {
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "platform": platform.platform(),
        }