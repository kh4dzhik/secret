from cryptography.fernet import Fernet, InvalidToken
from passlib.context import CryptContext

from app.core.config import settings

class CryptoService:
    # Сервис для шифрования и хеширования
    
    def __init__(self):
        self.fernet = Fernet(settings.SECRET_ENCRYPTION_KEY.encode())
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    def encrypt(self, data: str) -> bytes:
        return self.fernet.encrypt(data.encode())
    
    def decrypt(self, encrypted_data: bytes) -> str:
        try:
            return self.fernet.decrypt(encrypted_data).decode()
        except InvalidToken:
            raise ValueError("Ошибка дешифрования")
    
    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)
    
    def verify_password(self, password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(password, hashed_password)

# инициализация сервиса
crypto_service = CryptoService()