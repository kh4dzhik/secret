import redis
from datetime import timedelta
from uuid import UUID
from app.config import settings
from app.services.crypto import crypto_service


class RedisStorage:
    def __init__(self):
        self.client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            decode_responses=False,
            socket_connect_timeout=2
        )

    def cache_secret(self, secret_id: UUID, secret: str, ttl: int) -> bool:
        return bool(self.client.setex(
            f"secret:{secret_id}",
            timedelta(seconds=ttl),
            crypto_service.encrypt(secret)
        )

    def get_cached_secret(self, secret_id: UUID) -> str | None:
        encrypted = self.client.get(f"secret:{secret_id}")
        if encrypted:
            self.client.delete(f"secret:{secret_id}")
            return crypto_service.decrypt(encrypted)
        return None

redis_storage = RedisStorage()