from src.llms.registry.llm_registry import llm_registry

class LLMFactory:

    @staticmethod
    def create(name: str, **kwargs):
        llm_cls = llm_registry.get(name)
        return llm_cls(**kwargs)