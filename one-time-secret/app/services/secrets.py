from datetime import datetime, timedelta
from uuid import UUID
from sqlalchemy.orm import Session
from app.db.repositories.secrets import SecretRepository
from app.db.repositories.logs import LogRepository
from app.services.crypto import crypto_service
from app.storage.redis import redis_storage
from app.exceptions import NotFoundError, AlreadyAccessedError, ExpiredSecretError


class SecretService:
    def __init__(self, db: Session):
        self.secret_repo = SecretRepository(db)
        self.log_repo = LogRepository(db)

    def create_secret(self, secret: str, passphrase: str | None, ttl_seconds: int | None, ip: str, user_agent: str) -> UUID:
        expires_at = datetime.utcnow() + timedelta(seconds=ttl_seconds) if ttl_seconds else None
        
        secret_obj = self.secret_repo.create(
            encrypted_secret=crypto_service.encrypt(secret),
            passphrase_hash=crypto_service.hash_password(passphrase) if passphrase else None,
            expires_at=expires_at
        )
        
        self.log_repo.create_log(secret_obj.id, "create", ip, user_agent)
        redis_storage.cache_secret(secret_obj.id, secret, max(300, ttl_seconds) if ttl_seconds else 300)
        
        return secret_obj.id

    def get_secret(self, secret_id: UUID, ip: str, user_agent: str) -> str:
        cached = redis_storage.get_cached_secret(secret_id)
        if cached:
            self.log_repo.create_log(secret_id, "read_cache", ip, user_agent)
            return cached

        secret = self.secret_repo.get_by_id(secret_id)
        if not secret:
            raise NotFoundError()
        if secret.is_retrieved:
            raise AlreadyAccessedError()
        if secret.expires_at and secret.expires_at < datetime.utcnow():
            raise ExpiredSecretError()

        decrypted = crypto_service.decrypt(secret.encrypted_secret)
        self.secret_repo.mark_as_retrieved(secret_id)
        self.log_repo.create_log(secret_id, "read_db", ip, user_agent)
        
        return decrypted