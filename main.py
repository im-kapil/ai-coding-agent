import asyncio
from src.agents import CodingAgent
from src.graph.state import AgentState
from langchain_core.runnables import RunnableConfig
from src.graph.graph_factory import GraphFactory

async def main():

    graph = await GraphFactory.build()
    
    config: RunnableConfig = {"configurable": {"thread_id": "thread_123"}}

    result = await graph.ainvoke({"user_prompt": "Can you setup me a boilerplate code template for nest.js application using TypeScript with knexjs as the database ORM and Swagger for API documentation?"}, config)

    print(result)

asyncio.run(main())