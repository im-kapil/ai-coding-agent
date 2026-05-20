from pathlib import Path
from typing import Optional
import aiofiles
from langchain.tools import tool

# @tool
async def write_file(
        path: str,
        content: str,
        append: bool = False,
        overwrite: bool = True,
        encoding: str = "utf-8",
    ):
        """Write content into a file."""
        try:
            file_path = Path(path)

            # Create parent directories if needed
            file_path.parent.mkdir(parents=True, exist_ok=True)

            # Prevent overwrite if disabled
            if file_path.exists() and not overwrite and not append:
                return {
                    "success": False,
                    "error": "File already exists",
                    "path": str(file_path)
                }

            mode = "a" if append else "w"

            # Async file writing
            async with aiofiles.open(
                file_path,
                mode=mode,
                encoding=encoding
            ) as f:
                await f.write(content)

            return {
                "success": True,
                "path": str(file_path.resolve()),
                "size": file_path.stat().st_size,
                "append": append,
                "encoding": encoding,
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "path": path,
            }
            
async def main():
    await write_file("example.txt", "Hello, World!", overwrite=True)
    

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())