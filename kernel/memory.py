from typing import Dict, List, Any

class MemorySegment:
    def __init__(self, key: str, value: Any, tags: List[str] = None):
        self.key = key
        self.value = value
        self.tags = tags or []

class MemoryManager:
    def __init__(self):
        self.working_memory: Dict[str, Any] = {}
        self.long_term_memory: List[MemorySegment] = []
        self.shared_memory: Dict[str, Any] = {}

    def write_working(self, key: str, val: Any):
        self.working_memory[key] = val

    def read_working(self, key: str) -> Any:
        return self.working_memory.get(key)

    def save_long_term(self, key: str, value: Any, tags: List[str] = None):
        self.long_term_memory.append(MemorySegment(key, value, tags))

    def semantic_search(self, query: str, top_k: int = 2) -> List[Dict[str, Any]]:
        query_tokens = set(query.lower().split())
        results = []
        for item in self.long_term_memory:
            item_tokens = set(str(item.value).lower().split()) | set(item.key.lower().split())
            intersection = query_tokens.intersection(item_tokens)
            score = len(intersection) / max(len(query_tokens | item_tokens), 1)
            results.append((score, item))
        results.sort(key=lambda x: x[0], reverse=True)
        return [{"key": r[1].key, "value": r[1].value, "score": r[0]} for r in results[:top_k] if r[0] > 0]
