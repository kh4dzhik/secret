from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class SecretCreate(BaseModel):
    secret: str = Field(..., min_length=1, max_length=10000)
    passphrase: Optional[str] = Field(None, min_length=4, max_length=100)
    ttl_seconds: Optional[int] = Field(None, ge=60, le=86400)

class SecretResponse(BaseModel):
    secret: str

class SecretKeyResponse(BaseModel):
    secret_key: str
    expires_at: Optional[datetime]