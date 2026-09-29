import threading
import time


class Scheduler:

    def __init__(self):

        self.jobs = {}

        self.running = False

        self.thread = None

    def add(
        self,
        name,
        interval,
        callback,
    ):

        if name in self.jobs:
            raise KeyError(
                f"Job exists: {name}"
            )

        self.jobs[name] = {
            "interval": interval,
            "callback": callback,
            "last_run": 0,
        }

    def remove(self, name):

        self.jobs.pop(
            name,
            None,
        )

    def start(self):

        if self.running:
            return

        self.running = True

        self.thread = threading.Thread(
            target=self._loop,
            daemon=True,
        )

        self.thread.start()

    def stop(self):

        self.running = False

        if self.thread:
            self.thread.join(
                timeout=2
            )

    def _loop(self):

        while self.running:

            now = time.time()

            for job in self.jobs.values():

                if (
                    now - job["last_run"]
                    >= job["interval"]
                ):

                    try:
                        job["callback"]()

                    finally:
                        job["last_run"] = now

            time.sleep(1)