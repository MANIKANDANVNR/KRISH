class ModelRouter:

    def __init__(self):
        self.providers = {}
        self.default = None

    def register(
        self,
        name,
        provider,
    ):

        self.providers[name] = provider

        if self.default is None:
            self.default = name

    def select(self, name=None):

        selected = name or self.default

        if selected is None:
            raise LookupError(
                "No model provider."
            )

        if selected not in self.providers:
            raise LookupError(
                f"Unknown provider: {selected}"
            )

        return self.providers[selected]

    def health(self):

        return {
            name: provider.health()
            for name, provider
            in self.providers.items()
        }