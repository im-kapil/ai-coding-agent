from typing import Protocol, Dict, Any

class AgentProtocol(Protocol):
    name: str

    async def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        ...