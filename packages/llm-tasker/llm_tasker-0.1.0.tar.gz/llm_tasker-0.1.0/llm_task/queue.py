import abc
from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class BaseQueue(abc.ABC, Generic[T]):
    @abc.abstractmethod
    async def connect(self, **kwargs) -> None:
        """
        Method for initialization of the connection to the queue.
        The settings of the connection can vary depending on the system.
        """
        pass

    @abc.abstractmethod
    async def enqueue(self, message: T) -> None:
        """
        Asynchronous method for adding a message to the queue.
        :param message: The message that will be added to the queue.
        """
        pass

    @abc.abstractmethod
    async def dequeue(self) -> T:
        """
        Asynchronous method for extracting a message from the queue.
        :return: The message that was extracted from the queue.
        """
        pass

    @abc.abstractmethod
    async def close(self) -> None:
        """
        Method for closing the connection to the queue.
        """
        pass
