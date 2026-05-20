from pyexpat import model
from pyexpat.errors import messages
from typing import Any

from langchain.chat_models import init_chat_model
from langchain_ollama import ChatOllama
from ollama import chat
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from dotenv import load_dotenv
import os

load_dotenv()

def base_model():
    """Model Configuration

    Returns:
        _type_: Model intstance
    """
    # return ChatOllama(
    #     model="qwen2.5",
    #     validate_model_on_init=True,
    #     temperature=0,
    #     ).bind_tools([])
    
    return ChatNVIDIA(
            model="openai/gpt-oss-120b",
            api_key=os.getenv("NVIDIA_MODEL_API_KEY"),
            temperature=0,
            # top_p=1,
            max_tokens=4096,
        )

def base_model_chat(model, messages: list, response_format):
   try:
       response = chat(
           model=model,     
           messages= messages,
           format=response_format.model_json_schema(),
           options={'temperature': 0},
        )
       return response
   
   except Exception as e:
       print("Error in base_model_chat: ", e)
       return {
           "errors": str(e)
        }

def nvidia_base_model(messages: list, response_format: Any):
    """Model Configuration

    Returns:
        _type_: Model intstance
    """
    try:
        client = ChatNVIDIA(
            model="openai/gpt-oss-120b",
            api_key=os.getenv("NVIDIA_MODEL_API_KEY"),
            temperature=0,
            # top_p=1,
            max_tokens=4096,
            )
        return client.invoke(messages)
        
    except Exception as e:
       print("Error in nvidia_base_model: ", e)
       return {
           "errors": str(e)
        }