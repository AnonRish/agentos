import uuid
import copy
from enum import Enum
from typing import Dict, Any, List, Optional

class ProcessState(Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    PAUSED = "PAUSED"
    SLEEPING = "SLEEPING"
    TERMINATED = "TERMINATED"

class ProcessControlBlock:
    def __init__(self, pid: int, uuid_str: str, role: str, goals: List[str], skills: List[str], budget: float):
        self.pid = pid
        self.uuid = uuid_str
        self.role = role
        self.goals = goals
        self.skills = skills
        self.permissions: List[str] = []
        self.budget = budget
        self.model_preference = "gpt-4o"
        self.trust_score = 1.0
        self.state = ProcessState.PENDING
        self.metrics = {"tokens_used": 0, "cost": 0.0, "execution_time": 0.0}
        self.checkpoints: Dict[str, Dict[str, Any]] = {}

class AgentProcess:
    def __init__(self, pcb: ProcessControlBlock, memory=None):
        self.pcb = pcb
        self.memory = memory or {}
        self.context: Dict[str, Any] = {}

    def fork(self, new_pid: int) -> 'AgentProcess':
        new_pcb = copy.deepcopy(self.pcb)
        new_pcb.pid = new_pid
        new_pcb.uuid = str(uuid.uuid4())
        new_pcb.state = ProcessState.PENDING
        new_mem = copy.deepcopy(self.memory)
        return AgentProcess(new_pcb, new_mem)

    def checkpoint(self, checkpoint_id: str):
        snapshot = {
            "state": self.pcb.state.value,
            "memory": copy.deepcopy(self.memory),
            "context": copy.deepcopy(self.context),
            "metrics": copy.deepcopy(self.pcb.metrics)
        }
        self.pcb.checkpoints[checkpoint_id] = snapshot

    def rollback(self, checkpoint_id: str):
        if checkpoint_id not in self.pcb.checkpoints:
            raise ValueError(f"Checkpoint {checkpoint_id} not found.")
        snapshot = self.pcb.checkpoints[checkpoint_id]
        self.pcb.state = ProcessState(snapshot["state"])
        self.memory = copy.deepcopy(snapshot["memory"])
        self.context = copy.deepcopy(snapshot["context"])
        self.pcb.metrics = copy.deepcopy(snapshot["metrics"])
