import asyncio
from typing import Dict
from .process import AgentProcess, ProcessState

class AgentScheduler:
    def __init__(self):
        self.ready_queue = asyncio.Queue()
        self.processes: Dict[int, AgentProcess] = {}
        self._running = False

    def register_process(self, process: AgentProcess):
        self.processes[process.pcb.pid] = process
        self.ready_queue.put_nowait(process.pcb.pid)

    async def run_loop(self):
        self._running = True
        while self._running:
            if self.ready_queue.empty():
                await asyncio.sleep(0.05)
                continue
            pid = await self.ready_queue.get()
            process = self.processes.get(pid)
            if not process or process.pcb.state in (ProcessState.TERMINATED, ProcessState.PAUSED):
                continue
            
            process.pcb.state = ProcessState.RUNNING
            await self._execute_timeslice(process)
            
            if process.pcb.state == ProcessState.RUNNING:
                process.pcb.state = ProcessState.PENDING
                await self.ready_queue.put(pid)
            self.ready_queue.task_done()

    async def _execute_timeslice(self, process: AgentProcess):
        process.pcb.metrics["tokens_used"] += 120
        process.pcb.metrics["cost"] += 0.002
        await asyncio.sleep(0.01)

    def stop(self):
        self._running = False
