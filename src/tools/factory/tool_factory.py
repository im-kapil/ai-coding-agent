from src.tools.registry.tool_registry import tool_registry

class ToolFactory:

    @staticmethod
    def create(name: str, **kwargs):
        tool_cls = tool_registry.get(name)
        return tool_cls(**kwargs)