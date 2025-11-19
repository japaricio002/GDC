from fastmcp import FastMCP
from pathlib import Path
import os

# 1. Create the FastMCP server instance
mcp = FastMCP("Desktop Explorer")

# 2. Define a tool using the decorator
@mcp.tool()
def list_desktop_files(folder_name: str = "") -> str:
    """
    Lists filenames in a specific folder on the user's Desktop. 
    
    Args:
        folder_name: The name of the folder on the Desktop to check. 
                     If empty, lists files directly on the Desktop.
    """
    try:
        # Get the path to the user's Desktop in a cross-platform way
        desktop_path = Path.home() / "Desktop"
        
        # If a specific folder was requested, append it to the path
        target_path = desktop_path
        if folder_name:
            target_path = desktop_path / folder_name

        # Check if path exists
        if not target_path.exists():
            return f"Error: The folder '{target_path}' does not exist."

        # List the files
        files = []
        for item in target_path.iterdir():
            if item.is_file():
                files.append(item.name)
            elif item.is_dir():
                files.append(f"[DIR] {item.name}")

        if not files:
            return "The folder is empty."

        # Join the list into a readable string
        return "\n".join(files)

    except PermissionError:
        return "Error: Permission denied. The script doesn't have access to that folder."
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"
    
if __name__ == "__main__":
    mcp.run(transport="sse")