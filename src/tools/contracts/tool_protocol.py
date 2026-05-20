from typing import Protocol, Any

class ToolProtocol(Protocol):
    name: str
    description: str

    async def execute(self, *args, **kwargs) -> Any:
        ...