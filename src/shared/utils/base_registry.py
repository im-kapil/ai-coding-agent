from typing import Dict, Any

class BaseRegistry:
    def __init__(self):
        self._items: Dict[str, Any] = {}

    def register(self, name: str, item: Any):
        self._items[name] = item

    def get(self, name: str):
        if name not in self._items:
            raise ValueError(f"{name} not found")
        return self._items[name]

    def list(self):
        return list(self._items.keys())