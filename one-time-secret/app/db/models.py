from datetime import datetime
from sqlalchemy import Column, String, DateTime, Boolean, LargeBinary
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.db.session import Base


class Secret(Base):
    __tablename__ = "secrets"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())
    encrypted_secret = Column(LargeBinary, nullable=False)
    passphrase_hash = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    expires_at = Column(DateTime)
    is_retrieved = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=False)


class AccessLog(Base):
    __tablename__ = "access_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())
    secret_id = Column(UUID(as_uuid=True), nullable=False)
    action = Column(String(20), nullable=False)
    ip_address = Column(String(45))
    user_agent = Column(String)
    created_at = Column(DateTime, server_default=func.now())