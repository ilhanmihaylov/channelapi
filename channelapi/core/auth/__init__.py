import aioredis
import asyncio
import logging
from tornado.options import options
import secrets
import core.utils as utils
import datetime

logger = logging.getLogger("tornado.general")

class AuthManager:

    redis_client = None


    def __init__(self) -> None:
        self.redis_client = aioredis.from_url(f"redis://{options.redis_host}:{int(options.redis_port)}", encoding="utf-8", decode_responses=True)


    def generate_token(self, length:int = 32) -> str:
        return secrets.token_urlsafe(length)


    async def create_or_get_channel_token(self, channel):
        current = await self.redis_client.hgetall(f"channel:{channel}")
        if current and current.get('token'):
            return current.get('token')

        token = self.generate_token(32)
        now = utils.get_now()
        token_data = dict(created_at=now, token=token, channel=channel)
        channel_data = dict(token=token, created_at=now)
        await self.redis_client.hmset(f"channel:{channel}", channel_data)
        await self.redis_client.hmset(f"token:{token}", token_data)
        await self.redis_client.expire(f"channel:{channel}", 7*86400)
        await self.redis_client.expire(f"token:{token}", 7*86400)

        return token


    async def get_channel_from_token(self, token) -> str:
        current = await self.redis_client.hgetall(f"token:{token}")
        logger.debug('*' * 25)
        logger.debug(current)
        if current and current.get('channel'):
            return current.get('channel')


    async def token_connect(self, token) -> None:
        current = await self.redis_client.hgetall(f"token:{token}")
        if current and current.get('channel'):
            await self.redis_client.expire(f"token:{token}", 7*86400)
            await self.redis_client.expire(f"channel:{current.get('channel')}", 7*86400)
            await self.redis_client.hset(f"token:{token}", "last_connect_time", utils.get_now())


    async def describe_channel(self, channel):
        current = await self.redis_client.hgetall(f"channel:{channel}")
        if not current:
            return None
        token = await self.redis_client.hgetall(f"token:{current.get('token')}")
        current.update(token)
        return current
