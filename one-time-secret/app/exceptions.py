
class NotFoundError(Exception):
    """когда секрет не найден"""
    pass

class AlreadyAccessedError(Exception):
    """когда секрет уже был получен"""
    pass

class InvalidPassphraseError(Exception):
    """когда неверная парольная фраза"""
    pass

class ExpiredSecretError(Exception):
    """когда срок действия секрета истек"""
    pass