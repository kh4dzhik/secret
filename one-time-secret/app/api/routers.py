from fastapi import APIRouter
from app.api.endpoints import health, secrets

api_router = APIRouter()

api_router.include_router(secrets.router, prefix="/secret", tags=["secrets"])