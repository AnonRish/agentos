class SecurityEngine:
    def __init__(self):
        self._permissions: dict[int, set[str]] = {}

    def grant_permission(self, pid: int, capability: str):
        if pid not in self._permissions:
            self._permissions[pid] = set()
        self._permissions[pid].add(capability)

    def check_permission(self, pid: int, capability: str) -> bool:
        return capability in self._permissions.get(pid, set())
