class ServiceRegistry:

    def __init__(self):
        self._services = {}

    def register(self, name, service):

        if name in self._services:
            raise KeyError(
                f"Service already exists: {name}"
            )

        self._services[name] = service

    def replace(self, name, service):
        self._services[name] = service

    def get(self, name):
        if name not in self._services:
            raise KeyError(
                f"Unknown service: {name}"
            )

        return self._services[name]

    def has(self, name):
        return name in self._services

    def names(self):
        return tuple(
            sorted(self._services.keys())
        )