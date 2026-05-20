from src.agents.registry.agent_registry import agent_registry
from src.agents.coding.coding_agent import CodingAgent

agent_registry.register("coding_agent", CodingAgent)