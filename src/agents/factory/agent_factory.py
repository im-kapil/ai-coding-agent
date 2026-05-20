from src.agents.registry.agent_registry import agent_registry

class AgentFactory:

    @staticmethod
    def create(name: str, **kwargs):
        agent_cls = agent_registry.get(name)
        return agent_cls(**kwargs)