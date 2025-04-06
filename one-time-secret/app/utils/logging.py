import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from app.config import settings


def setup_logging():
    """Настройка логирования приложения"""
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            RotatingFileHandler(
                logs_dir / "app.log",
                maxBytes=1024 * 1024 * 5,  # 5 MB
                backupCount=3
            ),
            logging.StreamHandler()
        ]
    )