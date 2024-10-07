import asyncio
import logging
from collections.abc import Awaitable
from typing import Generic, TypeVar, Callable

from nonebot.log import logger as _logger

_T = TypeVar("_T")
LogListener = Callable[..., Awaitable[None]]


class LogStorage(Generic[_T]):
    def __init__(self, rotation: float = 5 * 60):
        self.count, self.rotation = 0, rotation
        self.logs: dict[int, _T] = {}
        self.listeners: set[LogListener] = set()

    async def add(self, log: _T):
        seq = self.count = self.count + 1
        self.logs[seq] = log
        asyncio.get_running_loop().call_later(self.rotation, self.remove, seq)
        await asyncio.gather(
            *(listener(log) for listener in self.listeners),
            return_exceptions=True,
        )
        return seq

    def remove(self, seq: int):
        del self.logs[seq]
        return

    def list(self, reverse: bool = False) -> list[_T]:
        return [self.logs[seq] for seq in sorted(self.logs, reverse=reverse)]


logging.getLogger("nonebot")

LOG_STORAGE = LogStorage[str]()
logger = _logger.opt(colors=True)
