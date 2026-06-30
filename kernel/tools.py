import asyncio
from typing import Callable, Dict, Any
from .security import SecurityEngine

class Tool:
    def __init__(self, name: str, func: Callable, required_capability: str):
        self.name = name
        self.func = func
        self.required_capability = required_capability

class ToolRuntime:
    def __init__(self, security_engine: SecurityEngine):
        self.tools: Dict[str, Tool] = {}
        self.security_engine = security_engine

    def register_tool(self, name: str, func: Callable, required_capability: str):
        self.tools[name] = Tool(name, func, required_capability)

    async def invoke(self, pid: int, name: str, **kwargs) -> Any:
        tool = self.tools.get(name)
        if not tool:
            raise FileNotFoundError(f"Tool {name} not found in execution runtime.")
        
        if not self.security_engine.check_permission(pid, tool.required_capability):
            raise PermissionError(f"PID {pid} lacks required capability: {tool.required_capability}")
        
        if asyncio.iscoroutinefunction(tool.func):
            return await tool.func(**kwargs)
        return tool.func(**kwargs)
