from src.core.base_agent import BaseAgent
from src.core.helpers.agent_response_formats import PlannerAgentResponseFormat
from src.core.prompts.planner_prompt import PLANNER_AGENT_SYSTEM_PROMPT
from src.llms.base_llm import base_model_chat, nvidia_base_model

class PlannerAgent(BaseAgent):
    async def execute(self, state):
        try:
            messages= [{
                'role': 'system',
                'content': PLANNER_AGENT_SYSTEM_PROMPT
            }, {
                'role': 'user',
                'content': state["user_prompt"]
            }]
                    
            # response = base_model_chat(
            #     model="qwen2.5",
            #     messages=messages,
            #     response_format=PlannerAgentResponseFormat
            # )
            
            response = nvidia_base_model(
                # model="openai/gpt-oss-120b",
                messages=messages,
                response_format=PlannerAgentResponseFormat
            )
                    
            print(f"[{self.name}] Generated plan: ", response.content)
            
            return {
                "plan": response.content,
                "current_agent": self.name
            }
        except Exception as e:
            print(f"[{self.name}] Error: {e}")
            return {
                "errors": str(e)
            }