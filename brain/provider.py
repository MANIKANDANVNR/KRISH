from abc import ABC, abstractmethod
from threading import Event


class ModelProvider(ABC):

    @abstractmethod
    def generate(
        self,
        messages,
        **kwargs,
    ):
        raise NotImplementedError

    def stream(
        self,
        messages,
        **kwargs,
    ):
        """
        Optional streaming interface.

        Providers that support streaming should override this
        method.

        `cancel_event` may be supplied by the caller. Providers
        should stop producing output when it is set.
        """

        raise NotImplementedError(
            "This provider does not support streaming."
        )

    def health(self):
        return False

    def cancel(self):
        """
        Optional provider-level cancellation hook.

        Providers with their own cancellation mechanism may
        override this method.
        """

        return False