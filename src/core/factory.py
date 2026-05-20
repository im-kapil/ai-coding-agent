from .registry import Registry

class AgentFactory:
    @staticmethod
    def create_agent(agent_name: str, llm_key: str):
        registry = Registry()  # Assuming Registry is a singleton or has class methods
        agent_cls = registry.get_agent(agent_name)
        llm = registry._llms.get(llm_key)
        
        if not agent_cls or not llm:
            raise ValueError(f"Agent {agent_name} or LLM {llm_key} not registered.")
        
        # Initialize the agent with tools from the registry
        return agent_cls(llm=llm, tools=registry.get_all_tools())