import redis
from src.config import Config

JTI_EXPIRY = 3600

token_blocklist = redis.Redis(
    host=Config.REDIS_HOST, port=Config.REDIS_PORT, db=0, protocol=3
)


def add_jti_to_blocklist(jti: str) -> None:
    token_blocklist.set(jti, "", ex=JTI_EXPIRY)


def token_in_blocklist(jti: str) -> bool:
    jti = token_blocklist.get(jti)
    return jti is not None
