# test_basic.py
from config.model_config import ModelConfig
from tools.file_operations import FileWriteTool

# Test model configuration
config = ModelConfig()
model = config.get_model_for_role("backend_developer")
print(f"✅ Model configured: {model.model}")

# Test file operations  
tool = FileWriteTool()
result = tool._run("test.txt", "Hello World!")
print(f"✅ File operation: {result}")
