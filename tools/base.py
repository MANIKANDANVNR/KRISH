from abc import ABC, abstractmethod


class Tool(ABC):

    name = "tool"

    permission = "tool"

    risk = "low"

    description = ""

    @abstractmethod
    def execute(self, **kwargs):
        raise NotImplementedError