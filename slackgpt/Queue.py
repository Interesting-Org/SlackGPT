from typing import Any

class Queue:
    def __init__(self):
        """Represents a queue of items
        """
        self.__queue = []

    def push(self, item):
        """Adds an item into the queue

        Args:
            item (Any): The item to be added
        """
        self.__queue.append(item)

    def pop(self):
        """Returns the first item in the queue

        Returns:
            Any: The first item in the queue
        """
        return self.__queue.pop(0)

    def insert(self, index, item):
        """Inserts an item at a specific index

        Args:
            index (int): The index to insert the item at
            item (Any): The item to insert
        """
        self.__queue.insert(index, item)

    def __len__(self) -> int:
        """The lenght of the queue

        Returns:
            int: The lenght of the queue
        """
        return len(self.__queue)

    def __getitem__(self, index) -> Any:
        return self.__queue[index]

