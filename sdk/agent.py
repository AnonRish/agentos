from typing import List, Optional
from ..kernel.process import AgentProcess, ProcessControlBlock

class Agent:
    def __init__(self, role: str, goals: List[str], skills: List[str], budget: float = 100.0, model: str = "gpt-4o"):
        self.role = role
        self.goals = goals
        self.skills = skills
        self.budget = budget
        self.model = model
        self.pid: Optional[int] = None
        self.process: Optional[AgentProcess] = None

    def to_process(self, pid: int) -> AgentProcess:
        pcb = ProcessControlBlock(
            pid=pid,
            uuid_str="",
            role=self.role,
            goals=self.goals,
            skills=self.skills,
            budget=self.budget
        )
        pcb.model_preference = self.model
        self.process = AgentProcess(pcb)
        self.pid = pid
        return self.process
