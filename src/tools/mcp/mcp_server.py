from fastapi import FastAPI

app = FastAPI()

@app.get("/mcp/tools")
async def tools():
    return {
        "tools": [
            "write_file",
            "terminal",
            "git"
        ]
    }