import os
from dotenv import load_dotenv
from qwen_agent.llm import get_chat_model
from typing_extensions import Any
import requests
from utils.loggers import Logger

load_dotenv()


class Qwen2:

    def __init__(self):
        self.host = os.getenv("OLLAMA_HOST") #Self hosted ollama host endppint 
        self.enable_thinking = os.getenv("ENABLE_THINKING") # Set this to true for more deeper insights
        self.enable_chat_stream = os.getenv("ENABLE_CHAT_STREAM") #Enable chat stream 
        self.logger = Logger(__file__)
        
        if not self.host:
            raise ValueError("LLm Host is not configured")
        
    def get_llm(self) -> Any:
        
        self.logger.log("executing [get_llm]")  
        model_config = {
            "model": "qwen2.5",
            "model_server": self.host,
            "api_key": "EMPTY",
            "generate_cfg": {
                "extra_body": {
                "chat_template_kwargs": {"enable_thinking": self.enable_thinking}  # default to True
            }
        }}
            
        return get_chat_model(model_config)

    # Design decision: able to execute parallet tolls call
    
    def process_query(self, query: str, tools: dict[str, Any]) -> dict[str, Any]:
        
        self.logger.log("executing [process_query]")  
            
        if not len(tools):
            payload = {
                "model": "qwen2.5",
                "prompt": query
            }
            
            response = requests.post(
                self.host+"/api/generate",
                json=payload,
                stream=True
                )
            return response