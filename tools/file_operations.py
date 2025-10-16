import os
from pathlib import Path
from crewai.tools import BaseTool

class FileWriteTool(BaseTool):
    name: str = "File Write Tool"
    description: str = "Writes content to a specified file in the workspace."

    def _run(self, file_path: str, content: str) -> str:
        try:
            full_path = Path(file_path)
            full_path.parent.mkdir(parents=True, exist_ok=True)

            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return f"✅ Successfully wrote to {file_path}"
        except Exception as e:
            return f"❌ Error writing to file: {str(e)}"

class ReadFileTool(BaseTool):
    name: str = "Read File Tool"
    description: str = "Reads the content of a specified file."

    def _run(self, file_path: str) -> str:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return f"📖 File content:\n{content}"
        except FileNotFoundError:
            return f"❌ File not found: {file_path}"
        except Exception as e:
            return f"❌ Error reading file: {str(e)}"

class ListDirectoryTool(BaseTool):
    name: str = "List Directory Tool"
    description: str = "Lists contents of a directory."

    def _run(self, directory_path: str = ".") -> str:
        try:
            path = Path(directory_path)
            if not path.exists():
                return f"❌ Directory does not exist: {directory_path}"

            items = []
            for item in sorted(path.iterdir()):
                if item.is_file():
                    size = item.stat().st_size
                    items.append(f"📄 {item.name} ({size} bytes)")
                else:
                    items.append(f"📁 {item.name}/")

            return f"📂 Directory contents:\n" + "\n".join(items)
        except Exception as e:
            return f"❌ Error listing directory: {str(e)}"