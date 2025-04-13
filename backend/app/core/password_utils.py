from argon2 import PasswordHasher
from argon2.exceptions import VerificationError, VerifyMismatchError


def hash_password(password: str) -> str:
    """Хеширует пароль."""
    ph = PasswordHasher()
    return ph.hash(password)


def verify_password(hashed_password: str, plain_password: str) -> bool:
    """Проверяет пароль."""
    try:
        ph = PasswordHasher()
        ph.verify(hashed_password, plain_password)
        return True
    except VerifyMismatchError:
        return False
    except VerificationError:
        return False
