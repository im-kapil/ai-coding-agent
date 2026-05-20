from typing import Any, Dict, List
from mcp.server.fastmcp import FastMCP
# from tavily import TavilyClient
import os
from dotenv import load_dotenv
import subprocess
import logging
from logging.handlers import RotatingFileHandler

load_dotenv()

# =========================================================
# Logging Configuration
# =========================================================

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

logger = logging.getLogger("mcp_server")
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    "[%(asctime)s] [%(levelname)s] %(message)s"
)

# Console Logs
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

# File Logs
file_handler = RotatingFileHandler(
    f"{LOG_DIR}/mcp_server.log",
    maxBytes=5 * 1024 * 1024,  # 5 MB
    backupCount=5
)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)

logger.info("Starting MCP Server initialization...")

# =========================================================
# MCP Server
# =========================================================

mcp = FastMCP(
    name="AI Coding agent MCP server",
    host="0.0.0.0",
    port=9009,
)

logger.info("MCP Server initialized successfully")

# =========================================================
# Tools
# =========================================================

@mcp.tool(
    name="create_directory",
    description="Create a directory at the given path",
    structured_output=True
)
def create_directory(path: str) -> Dict[str, Any]:
    logger.info(f"[create_directory] Requested path: {path}")

    try:
        os.makedirs(path, exist_ok=True)

        logger.info(f"[create_directory] Directory created successfully: {path}")

        return {
            "success": True,
            "message": f"Directory created: {path}"
        }

    except Exception as e:
        logger.exception(f"[create_directory] Failed for path: {path}")

        return {
            "success": False,
            "error": str(e)
        }


@mcp.tool(
    name="create_file",
    description="Create a file with optional content",
    structured_output=True
)
def create_file(path: str, content: str = "") -> Dict[str, Any]:
    logger.info(f"[create_file] Creating file: {path}")

    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)

        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

        logger.info(
            f"[create_file] File created successfully: {path} "
            f"(content length: {len(content)})"
        )

        return {
            "success": True,
            "message": f"File created: {path}"
        }

    except Exception as e:
        logger.exception(f"[create_file] Failed for file: {path}")

        return {
            "success": False,
            "error": str(e)
        }


@mcp.tool(
    name="read_file",
    description="Read contents of a file",
    structured_output=True
)
def read_file(path: str) -> Dict[str, Any]:
    logger.info(f"[read_file] Reading file: {path}")

    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        logger.info(
            f"[read_file] Successfully read file: {path} "
            f"(content length: {len(content)})"
        )

        return {
            "success": True,
            "content": content
        }

    except Exception as e:
        logger.exception(f"[read_file] Failed reading file: {path}")

        return {
            "success": False,
            "error": str(e)
        }


@mcp.tool(
    name="update_file",
    description="Overwrite or update a file",
    structured_output=True
)
def update_file(path: str, content: str) -> Dict[str, Any]:
    logger.info(f"[update_file] Updating file: {path}")

    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

        logger.info(
            f"[update_file] File updated successfully: {path} "
            f"(content length: {len(content)})"
        )

        return {
            "success": True,
            "message": f"File updated: {path}"
        }

    except Exception as e:
        logger.exception(f"[update_file] Failed updating file: {path}")

        return {
            "success": False,
            "error": str(e)
        }


@mcp.tool(
    name="delete_file",
    description="Delete a file",
    structured_output=True
)
def delete_file(path: str) -> Dict[str, Any]:
    logger.info(f"[delete_file] Deleting file: {path}")

    try:
        os.remove(path)

        logger.info(f"[delete_file] File deleted successfully: {path}")

        return {
            "success": True,
            "message": f"Deleted file: {path}"
        }

    except Exception as e:
        logger.exception(f"[delete_file] Failed deleting file: {path}")

        return {
            "success": False,
            "error": str(e)
        }


@mcp.tool(
    name="list_files",
    description="List files in a directory",
    structured_output=True
)
def list_files(path: str) -> Dict[str, Any]:
    logger.info(f"[list_files] Listing files in: {path}")

    try:
        files = os.listdir(path)

        logger.info(
            f"[list_files] Found {len(files)} files/directories in: {path}"
        )

        return {
            "success": True,
            "files": files
        }

    except Exception as e:
        logger.exception(f"[list_files] Failed listing files in: {path}")

        return {
            "success": False,
            "error": str(e)
        }


@mcp.tool(
    name="file_exists",
    description="Check if file or directory exists",
    structured_output=True
)
def file_exists(path: str) -> Dict[str, Any]:
    logger.info(f"[file_exists] Checking path: {path}")

    exists = os.path.exists(path)

    logger.info(f"[file_exists] Exists={exists} for path: {path}")

    return {
        "success": True,
        "exists": exists
    }


@mcp.tool(
    name="run_command",
    description="Execute a shell command",
    structured_output=True
)
def run_command(command: str, cwd: str = None) -> Dict[str, Any]:
    logger.info(f"[run_command] Executing command: {command}")
    logger.info(f"[run_command] Working directory: {cwd}")

    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True
        )

        logger.info(
            f"[run_command] Command completed "
            f"(return code: {result.returncode})"
        )

        if result.stdout:
            logger.debug(f"[run_command][STDOUT]\n{result.stdout}")

        if result.stderr:
            logger.warning(f"[run_command][STDERR]\n{result.stderr}")

        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "return_code": result.returncode
        }

    except Exception as e:
        logger.exception(f"[run_command] Command failed: {command}")

        return {
            "success": False,
            "error": str(e)
        }


@mcp.tool(
    name="install_dependency",
    description="Install a dependency using npm or pip",
    structured_output=True
)
def install_dependency(name: str, manager: str = "npm") -> Dict[str, Any]:
    logger.info(
        f"[install_dependency] Installing dependency: {name} "
        f"using {manager}"
    )

    try:
        if manager == "npm":
            command = f"npm install {name}"

        elif manager == "pip":
            command = f"pip install {name}"

        else:
            logger.error(
                f"[install_dependency] Unsupported manager: {manager}"
            )

            return {
                "success": False,
                "error": "Unsupported package manager"
            }

        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True
        )

        logger.info(
            f"[install_dependency] Installation completed "
            f"(return code: {result.returncode})"
        )

        if result.stdout:
            logger.debug(f"[install_dependency][STDOUT]\n{result.stdout}")

        if result.stderr:
            logger.warning(f"[install_dependency][STDERR]\n{result.stderr}")

        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr
        }

    except Exception as e:
        logger.exception(
            f"[install_dependency] Failed installing dependency: {name}"
        )

        return {
            "success": False,
            "error": str(e)
        }


@mcp.tool(
    name="search_in_files",
    description="Search for a string inside files",
    structured_output=True
)
def search_in_files(path: str, query: str) -> Dict[str, Any]:
    logger.info(
        f"[search_in_files] Searching for '{query}' in path: {path}"
    )

    matches: List[Dict[str, Any]] = []

    try:
        for root, _, files in os.walk(path):

            logger.debug(
                f"[search_in_files] Scanning directory: {root}"
            )

            for file in files:
                file_path = os.path.join(root, file)

                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        for i, line in enumerate(f.readlines()):

                            if query in line:
                                match = {
                                    "file": file_path,
                                    "line_number": i + 1,
                                    "line": line.strip()
                                }

                                matches.append(match)

                                logger.debug(
                                    f"[search_in_files] Match found: "
                                    f"{file_path}:{i + 1}"
                                )

                except Exception as inner_error:
                    logger.warning(
                        f"[search_in_files] Skipping file "
                        f"{file_path}: {inner_error}"
                    )

                    continue

        logger.info(
            f"[search_in_files] Total matches found: {len(matches)}"
        )

        return {
            "success": True,
            "matches": matches
        }

    except Exception as e:
        logger.exception(
            f"[search_in_files] Search failed in path: {path}"
        )

        return {
            "success": False,
            "error": str(e)
        }


# =========================================================
# Main
# =========================================================

def main():
    logger.info("Starting MCP server on port 9009...")

    try:
        mcp.run(
            transport="streamable-http",
            mount_path="/mcp"
        )

    except Exception as e:
        logger.exception("Failed to start MCP server")


if __name__ == "__main__":
    main()