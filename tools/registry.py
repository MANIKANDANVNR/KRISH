class ToolRegistry:

    def __init__(self):
        self._tools = {}

    def register(self, tool):

        if tool.name in self._tools:
            raise KeyError(
                f"Tool exists: {tool.name}"
            )

        self._tools[tool.name] = tool

    def get(self, name):

        if name not in self._tools:
            raise KeyError(
                f"Unknown tool: {name}"
            )

        return self._tools[name]

    def list(self):

        return tuple(
            sorted(self._tools.keys())
        )