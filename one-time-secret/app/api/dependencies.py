from fastapi import Header, Depends
from typing import Optional

def get_user_agent(user_agent: Optional[str] = Header(None)) -> str:
    return user_agent or "unknown"

def get_client_ip(x_forwarded_for: Optional[str] = Header(None)) -> str:
    return x_forwarded_for.split(",")[0].strip() if x_forwarded_for else "unknown"