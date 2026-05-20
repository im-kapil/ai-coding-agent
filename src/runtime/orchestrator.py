class Orchestrator:

    async def run(self, workflow, state):
        return await workflow.ainvoke(state)