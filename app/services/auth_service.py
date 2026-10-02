
from app.security.jwt import hash_password, verify_password


def create_password_hash(password: str) -> str:
    return hash_password(password)


def check_password(
    plain_password: str,
    hashed_password: str
) -> bool:
    return verify_password(plain_password, hashed_password)