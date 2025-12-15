from collections import deque
from typing import Any, Optional


class Stack:
    """Стек на базе списка (LIFO - Last In, First Out)."""
    
    def __init__(self) -> None:
        self._data: list[Any] = []
    
    def push(self, item: Any) -> None:
        self._data.append(item)
    
    def pop(self) -> Any:
        if self.is_empty():
            raise IndexError("Pop from empty stack")
        return self._data.pop()
    
    def peek(self) -> Optional[Any]:
        return self._data[-1] if not self.is_empty() else None
    
    def is_empty(self) -> bool:
        return len(self._data) == 0
    
    def __len__(self) -> int:
        return len(self._data)
    
    def __repr__(self) -> str:
        return f"Stack({self._data})"


class Queue:
    """Очередь на базе collections.deque (FIFO - First In, First Out)."""
    
    def __init__(self) -> None:
        self._data: deque[Any] = deque()
    
    def enqueue(self, item: Any) -> None:
        self._data.append(item)
    
    def dequeue(self) -> Any:
        if self.is_empty():
            raise IndexError("Dequeue from empty queue")
        return self._data.popleft()
    
    def peek(self) -> Optional[Any]:
        return self._data[0] if not self.is_empty() else None
    
    def is_empty(self) -> bool:
        return len(self._data) == 0
    
    def __len__(self) -> int:
        return len(self._data)
    
    def __repr__(self) -> str:
        return f"Queue({list(self._data)})"