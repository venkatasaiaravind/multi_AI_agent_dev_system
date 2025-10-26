from pathlib import Path
from crewai.tools import tool

@tool("Write File Tool")
def write_file_tool(filepath: str, content: str) -> str:
    """
    Write content to a file.
    
    Args:
        filepath: Path to the file to write
        content: Content to write to the file
    
    Returns:
        Success message or error
    """
    try:
        file_path = Path(filepath)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8', errors='replace') as f:
            f.write(content)
        
        return f"✅ Successfully wrote {len(content)} characters to {filepath}"
    except Exception as e:
        return f"❌ Error writing file: {str(e)}"

@tool("Read File Tool")
def read_file_tool(filepath: str) -> str:
    """
    Read content from a file.
    
    Args:
        filepath: Path to the file to read
    
    Returns:
        File content or error message
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except Exception as e:
        return f"❌ Error reading file: {str(e)}"

@tool("List Directory Tool")
def list_directory_tool(dirpath: str) -> str:
    """
    List all files in a directory.
    
    Args:
        dirpath: Path to the directory
    
    Returns:
        List of files or error message
    """
    try:
        files = list(Path(dirpath).rglob("*"))
        return "\n".join([str(f) for f in files if f.is_file()])
    except Exception as e:
        return f"❌ Error listing directory: {str(e)}"


# Export as a list for easy importing
file_tools = [write_file_tool, read_file_tool, list_directory_tool]
