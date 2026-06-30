import asyncio
from typing import List
from ..kernel.process import AgentProcess, ProcessState
from ..kernel.scheduler import AgentScheduler
from ..kernel.ipc import MessageBus, Message
from ..kernel.security import SecurityEngine
from ..kernel.tools import ToolRuntime
from .agent import Agent

class AgentOS:
    def __init__(self):
        self.scheduler = AgentScheduler()
        self.message_bus = MessageBus()
        self.security_engine = SecurityEngine()
        self.tool_runtime = ToolRuntime(self.security_engine)
        self._next_pid = 1

    def create_team(self, agents: List[Agent]) -> List[AgentProcess]:
        processes = []
        for agent in agents:
            pid = self._next_pid
            self._next_pid += 1
            
            proc = agent.to_process(pid)
            self.security_engine.grant_permission(pid, "use_basic_tools")
            self.message_bus.register_channel(pid)
            self.scheduler.register_process(proc)
            processes.append(proc)
        return processes

    async def run_async(self, goal: str):
        print(f"[*] Initializing AgentOS Kernel with high-level goal: {goal}")
        scheduler_task = asyncio.create_task(self.scheduler.run_loop())
        
        for pid, proc in self.scheduler.processes.items():
            proc.pcb.state = ProcessState.PENDING
            print(f"[+] Booted PID {pid} [{proc.pcb.role}] - Ready to address target goals.")
        
        await asyncio.sleep(0.5)
        self.scheduler.stop()
        await scheduler_task
        print("[*] Goal execution complete. All agent sub-threads yielded control.")

    def run(self, goal: str):
        asyncio.run(self.run_async(goal))
