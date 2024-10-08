from typing import Generic, TypeVar

from pydantic import BaseModel
from llm_task.queues.base import BaseQueue

T = TypeVar("T", bound=BaseModel)

class RedisQueue(BaseQueue, Generic[T]):
    async def connect(self, url: str, queue_name: str, **redis_kwargs) -> None:
        try:
            from redis import asyncio as redis
        except ImportError:
            raise ImportError(
                "redis-py не установлен. "
                "Установите зависимости: pip install llm-task[redis]"
            )
        self._client = redis.Redis()

    async def enqueue(self, message: T) -> None:
        await self._redis.rpush(self._queue_name, message)

    async def dequeue(self) -> T:
        message = await self._redis.blpop(self._queue_name)
        return message[1] if message else None

    async def close(self) -> None:
        self._redis.close()
        await self._redis.wait_closed()
        
