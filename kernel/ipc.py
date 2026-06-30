import asyncio
from typing import Dict, List, Callable, Any

class Message:
    def __init__(self, sender_pid: int, receiver_pid: int, msg_type: str, payload: Dict[str, Any]):
        self.sender_pid = sender_pid
        self.receiver_pid = receiver_pid
        self.msg_type = msg_type
        self.payload = payload

class MessageBus:
    def __init__(self):
        self._subscribers: Dict[str, List[Callable[[Message], Any]]] = {}
        self._direct_channels: Dict[int, asyncio.Queue] = {}

    def register_channel(self, pid: int):
        self._direct_channels[pid] = asyncio.Queue()

    def subscribe(self, topic: str, callback: Callable[[Message], Any]):
        if topic not in self._subscribers:
            self._subscribers[topic] = []
        self._subscribers[topic].append(callback)

    async def publish(self, topic: str, message: Message):
        if topic in self._subscribers:
            for callback in self._subscribers[topic]:
                if asyncio.iscoroutinefunction(callback):
                    await callback(message)
                else:
                    callback(message)

    async def send_direct(self, message: Message):
        if message.receiver_pid in self._direct_channels:
            await self._direct_channels[message.receiver_pid].put(message)

    async def receive_direct(self, pid: int) -> Message:
        if pid not in self._direct_channels:
            raise ValueError(f"No direct channel registered for PID {pid}")
        return await self._direct_channels[pid].get()
