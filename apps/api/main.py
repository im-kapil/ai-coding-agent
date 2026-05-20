from fastapi import FastAPI

app = FastAPI(title="Agentic Coding Platform")

@app.get("/health")
async def health():
    return {"status": "healthy"}