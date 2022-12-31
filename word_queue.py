from typing import Any


class EmptyQueueError(Exception):
    def __str__(self) -> str:
        return 'Pop may not be called on an empty queue'


class Queue:
    items: list

    def __init__(self) -> None:
        """Initialize a new empty queue."""
        self._items = []

    def is_empty(self) -> bool:
        """Return whether this queue contains no items."""
        return self._items == []

    def enqueue(self, item: Any) -> None:
        """Add <item> to the back of this queue."""
        self._items.append(item)

    def dequeue(self) -> Any:
        """Remove and return the item at the front of this queue.
        """
        if self.is_empty():
            raise EmptyQueueError

        return self._items.pop(0)
