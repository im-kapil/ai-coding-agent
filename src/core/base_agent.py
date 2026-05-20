from abc import ABC, abstractmethod
from typing import Any

class BaseAgent(ABC):

    def __init__(self, name:str, tools: list, llm: Any):
        self.name = name
        self.tools = tools or []
        self.llm = llm

    async def __call__(self, state: dict) -> dict:
        """LangGraph expects callable nodes"""
        try:
            print(f"[{self.name}] Running")
            return await self.execute(state)
            # return await self.invoke(state)
        except Exception as e:
            print(f"[{self.name}] Error: {e}")
            raise

    @abstractmethod
    async def execute(self, state: dict) -> dict:
        pass