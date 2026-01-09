# 사용자 인증
import bcrypt
from sqlmodel import Session
from models import User
from users_service import get_user_by_username

def validate_user(username: str, plain_password: str, session: Session) -> User | None:
    
    user = get_user_by_username(username, session)
    if not user:
        return None
    
    plain_password_bytes = plain_password.encode('utf-8')
    hashed_password_bytes = user.password.encode('utf-8')

    if bcrypt.checkpw(plain_password_bytes, hashed_password_bytes):
        return user
    
    return None