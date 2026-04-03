from typing import Any, Dict, List
from mcp.server.fastmcp import FastMCP
# from tavily import TavilyClient
import os
from dotenv import load_dotenv
import subprocess

load_dotenv()


mcp = FastMCP(
    name="AI Coding agent MCP server",
    # description="this is a sample wether server",
    host="0.0.0.0",
    port=9009,
    # reload=True,
    )

@mcp.tool(
    name="create_directory",
    description="Create a directory at the given path",
    structured_output=True
)
def create_directory(path: str) -> Dict[str, Any]:
    try:
        os.makedirs(path, exist_ok=True)
        return {
            "success": True,
            "message": f"Directory created: {path}"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool(
    name="create_file",
    description="Create a file with optional content",
    structured_output=True
)
def create_file(path: str, content: str = "") -> Dict[str, Any]:
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

        return {
            "success": True,
            "message": f"File created: {path}"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}
    
@mcp.tool(
    name="read_file",
    description="Read contents of a file",
    structured_output=True
)
def read_file(path: str) -> Dict[str, Any]:
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        return {
            "success": True,
            "content": content
        }
    except Exception as e:
        return {"success": False, "error": str(e)}
    
@mcp.tool(
    name="update_file",
    description="Overwrite or update a file",
    structured_output=True
)
def update_file(path: str, content: str) -> Dict[str, Any]:
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

        return {
            "success": True,
            "message": f"File updated: {path}"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool(
    name="delete_file",
    description="Delete a file",
    structured_output=True
)
def delete_file(path: str) -> Dict[str, Any]:
    try:
        os.remove(path)
        return {
            "success": True,
            "message": f"Deleted file: {path}"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}
    
@mcp.tool(
    name="list_files",
    description="List files in a directory",
    structured_output=True
)
def list_files(path: str) -> Dict[str, Any]:
    try:
        files = os.listdir(path)
        return {
            "success": True,
            "files": files
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool(
    name="file_exists",
    description="Check if file or directory exists",
    structured_output=True
)
def file_exists(path: str) -> Dict[str, Any]:
    return {
        "success": True,
        "exists": os.path.exists(path)
    }
    
@mcp.tool(
    name="run_command",
    description="Execute a shell command",
    structured_output=True
)
def run_command(command: str, cwd: str = None) -> Dict[str, Any]:
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True
        )

        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "return_code": result.returncode
        }

    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool(
    name="install_dependency",
    description="Install a dependency using npm or pip",
    structured_output=True
)
def install_dependency(name: str, manager: str = "npm") -> Dict[str, Any]:
    try:
        if manager == "npm":
            command = f"npm install {name}"
        elif manager == "pip":
            command = f"pip install {name}"
        else:
            return {"success": False, "error": "Unsupported package manager"}

        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True
        )

        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr
        }

    except Exception as e:
        return {"success": False, "error": str(e)}
    
@mcp.tool(
    name="search_in_files",
    description="Search for a string inside files",
    structured_output=True
)
def search_in_files(path: str, query: str) -> Dict[str, Any]:
    matches: List[Dict[str, Any]] = []

    try:
        for root, _, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        for i, line in enumerate(f.readlines()):
                            if query in line:
                                matches.append({
                                    "file": file_path,
                                    "line_number": i + 1,
                                    "line": line.strip()
                                })
                except:
                    continue

        return {"success": True, "matches": matches}

    except Exception as e:
        return {"success": False, "error": str(e)}
    
def main():
    # Initialize and run the server
    # mcp.run(transport="stdio", mount_path="/mcp")
    mcp.run(transport="streamable-http", mount_path="/mcp")
    
if __name__ == "__main__":
    main()