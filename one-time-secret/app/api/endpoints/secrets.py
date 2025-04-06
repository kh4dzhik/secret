
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.responses import JSONResponse
from uuid import UUID
from app.services.secrets import SecretService
from app.db.session import get_db
from app.api.schemas.secrets import SecretCreate, SecretResponse, SecretKeyResponse
from app.api.dependencies import get_user_agent, get_client_ip
from app.exceptions import NotFoundError, AlreadyAccessedError, ExpiredSecretError

router = APIRouter()

@router.post("", response_model=SecretKeyResponse, status_code=201)
async def create_secret(
    request: Request,
    secret_data: SecretCreate,
    service: SecretService = Depends(),
    user_agent: str = Depends(get_user_agent),
    ip_address: str = Depends(get_client_ip)
):
    
    # создаем новый секрет
    try:
        secret_id = service.create_secret(
            secret=secret_data.secret,
            passphrase=secret_data.passphrase,
            ttl_seconds=secret_data.ttl_seconds,
            ip=ip_address,
            user_agent=user_agent
        )
        return {"secret_key": str(secret_id)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{secret_key}", response_model=SecretResponse)
async def get_secret(
    secret_key: UUID,
    response: Response,
    service: SecretService = Depends(),
    user_agent: str = Depends(get_user_agent),
    ip_address: str = Depends(get_client_ip)
):
    try:
        secret = service.get_secret(secret_key, ip_address, user_agent)

        # запрешаем кефирование 
        response.headers.update({
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0"
        })

        return {"secret": secret}
    
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Secret not found")
    except (AlreadyAccessedError, ExpiredSecretError):
        raise HTTPException(status_code=410, detail="Secret unavailable")