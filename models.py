import uuid
from datetime import datetime
from typing import Optional, List
from sqlmodel import Field, SQLModel, Session, create_engine, select, Relationship

class User(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    username: str = Field(unique=True, index=True)
    password: str # 저장된 비밀번호는 암호화된 해시로 들어감.

    comments: List["Comment"] = Relationship(back_populates="user")

class Post(SQLModel, table = True): # 상속, database.py에서 클래스 정의 다 해둠.
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key = True) 
    user_id: Optional[str] = Field(index=True)
    question: str
    answer: Optional[str] = Field(default=None, index= True) #Optional[]: 파이썬의 타이핑 시스템에서 사용함, 특정 변수의 값이 아무것도 없는 상태일 수도 있음을 명시할 때 씀, 빼면? 무조건 UUID 생성됨.
    created_at: datetime = Field(
        default_factory= datetime.now,
        nullable = False     
    )

    comments: List["Comment"] = Relationship(back_populates="post")

class Comment(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    
    content: str 
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)

    post_id: uuid.UUID = Field(foreign_key="post.id", index=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", index=True)

    post: Optional[Post] = Relationship(back_populates="comments")
    user: Optional[User] = Relationship(back_populates="comments")
       

sqlite_url = "sqlite:///ffaa.db"
engine = create_engine(sqlite_url)
# sqlite를 생성하는 SQLAlchemy 문법 '/' 3개는 상대경로 4개는 절대 경로를 뜻한다.

def create_db_and_tables():
    SQLModel.metadata.create.all(engine)

if __name__ == "__main__":
    create_db_and_tables()
    print("화긴!") 