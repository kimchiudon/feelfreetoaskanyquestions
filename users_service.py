# db 속 user 테이블 만들기
import bcrypt
from sqlmodel import Session, select
from models import User

def get_user_by_username(username: str, session: Session) -> User | None:

    statement = select(User).where(User.username == username)
    return session.exec(statement).first()

def create_user(user_data: dict, session: Session) -> User:

    password_bytes = user_data["password"].encode('utf-8')
    
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)

    new_user = User(
        username=user_data["username"],
        password=hashed_password.decode('utf-8')
    )

    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user