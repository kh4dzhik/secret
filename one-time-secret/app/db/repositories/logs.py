

class LogRepository:
    """репозиторий для работы с логами доступа"""
    
    def __init__(self, db: Session):
        self.db = db

    def create_log(
        self,
        secret_id: UUID,
        action: str,
        ip_address: str,
        user_agent: str = None
    ) -> None:

        log = AccessLog(
            secret_id=secret_id,
            action=action,
            ip_address=ip_address,
            user_agent=user_agent
        )
        self.db.add(log)
        self.db.commit()