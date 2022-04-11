from typing import Any, Set, Callable

import aioredis


class RedisStream:
    def __init__(self, redis_uri: str):
        self.redis_uri = redis_uri
        self.streams: Set = set()

    async def connect(self) -> None:
        self._conn = await aioredis.from_url(self.redis_uri, decode_responses=True)

    async def disconnect(self) -> None:
        await self._conn.close()

    async def publish(self, channel: str, msg: Any) -> None:
        await self.connect()
        await self._conn.xadd(channel, {"payload": msg})

    async def consume(self, channel: str, f_processor: Callable) -> None:
        await self.connect()
        while True:
            for _channel, payloads in await self._conn.xread({channel: "$"}, block=0):
                for _id, payload in payloads:
                    await f_processor(payload["payload"])
