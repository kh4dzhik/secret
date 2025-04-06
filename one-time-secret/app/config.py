import os
# from typing import Optional


class ConfigError(Exception):
    pass


# Получение обязательной переменной окружения

class Settings:
    """Класс конфигурации приложения"""
    
    def __init__(self):
        self.SECRET_ENCRYPTION_KEY = get_env("SECRET_ENCRYPTION_KEY")
        
        # redis
        self.REDIS_HOST = get_env("REDIS_HOST")
        self.REDIS_PORT = get_int_env("REDIS_PORT")
        
        # postgresql
        self.POSTGRES_HOST = get_env("POSTGRES_HOST")
        self.POSTGRES_PORT = get_env("POSTGRES_PORT")
        self.POSTGRES_DB = get_env("POSTGRES_DB")
        self.POSTGRES_USER = get_env("POSTGRES_USER")
        self.POSTGRES_PASSWORD = get_env("POSTGRES_PASSWORD")


        def get_env(self, name: str) -> str:
            value = os.getenv(name)
            if not value:
                raise ConfigError(f"Переменная окружения {name} не установлена")
            return value

        # Получение и проверка числовой переменной
        def get_int_env(self, name: str) -> int:
            value = self.get_env(name)
            try:
                return int(value)
            except ValueError:
                raise ConfigError(f"{name} должно быть числом")


        # дополнительные проверки
        if not 1 <= self.REDIS_PORT <= 65535:
            raise ConfigError("REDIS_PORT должен быть в диапазоне 1-65535")

        if not self.SECRET_ENCRYPTION_KEY:
            raise ConfigError("SECRET_ENCRYPTION_KEY must be set in environment") 


        @property
        def postgres_url(self) -> str:
            return (
                f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
                f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
            )
        

# Инициализация конфигурации
try:
    settings = Settings()
except ConfigError as e:
    raise RuntimeError(f"Ошибка конфигурации: {e}")