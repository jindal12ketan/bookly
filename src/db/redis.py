from redis.asyncio import Redis
from src.config import Config

JTI_EXPIRY = 3600  # 1 hour

redis_client: Redis = Redis(
    host=Config.REDIS_HOST,
    port=Config.REDIS_PORT,
    db=0,
    encoding="utf-8",
    decode_responses=True,  # to get string responses instead of bytes
)


async def add_jti_to_blocklist(jti: str) -> None:
    await redis_client.set(name=jti, value="", ex=JTI_EXPIRY)


async def token_in_blocklist(jti: str) -> bool:
    jti = await redis_client.get(name=jti)
    return jti is not None
