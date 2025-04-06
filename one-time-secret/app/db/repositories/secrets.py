from uuid import UUID
from datetime import datetime
from sqlalchemy.orm import Session

from app.db.models import Secret


class SecretRepository:
    """Репозиторий для работы с секретами в БД"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, secret_id: UUID) -> Secret | None:
        return self.db.query(Secret).filter(Secret.id == secret_id).first()
    
    def create(
        self,
        encrypted_secret: bytes,
        passphrase_hash: str | None = None,
        expires_at: datetime | None = None
    ) -> Secret:
        secret = Secret(
            encrypted_secret=encrypted_secret,
            passphrase_hash=passphrase_hash,
            expires_at=expires_at
        )
        self.db.add(secret)
        self.db.commit()
        self.db.refresh(secret)
        return secret
    
    
    def mark_as_retrieved(self, secret_id: UUID) -> None:
        secret = self.get_by_id(secret_id)
        if secret:
            secret.is_retrieved = True
            self.db.commit()
