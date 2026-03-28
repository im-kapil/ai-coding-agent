""" 
Planner for planning the task that agent need to execute
"""

from models.qwen2 import Qwen2
from typing import Any
from utils.loggers import Logger
import json
class Planner: 
    def __init__(self):
        self.logger = Logger(__file__)
    pass
    
    def create_plan(self, prompt: str) -> dict[str, Any]:
        self.logger.log("executing [create_plan]")
        # LLm
        llm = Qwen2()
        chat_response = llm.process_query(prompt, [])
        
        for line in chat_response.iter_lines():
            if line:
                chunk = json.loads(line)
                token = chunk.get("response", "")
                print(token, end="", flush=True)
                      
        return chat_response