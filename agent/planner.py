""" 
Planner for planning the task that agent need to execute
"""

from models.qwen2 import Qwen2
from typing import Any
from utils.loggers import Logger
import json
from prompts.planner_prompt import planner_prompt


class Planner: 
    def __init__(self):
        self.logger = Logger(__file__)
    pass
    
    def create_plan(self, prompt: str) -> dict[str, Any]:
        self.logger.log("executing [create_plan]")
        # LLm
        llm = Qwen2()
        
        prompt_formatted = planner_prompt.format(
        user_query=prompt,
        tools_list="create_file"
    )
        
        chat_response = llm.process_query(prompt_formatted, [])
                
        for line in chat_response.iter_lines():
            if line:
                chunk = json.loads(line)
                token = chunk.get("response", "")
                print(token, end="", flush=True)
                      
        return chat_response