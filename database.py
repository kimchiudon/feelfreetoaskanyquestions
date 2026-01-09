from sqlmodel import Field, Session, SQLModel, create_engine, select

from models import Post

sqlite_url = "sqlite:///ffaa.db"
engine = create_engine(sqlite_url, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine) #sqlmodel로 클래스 선언, db 만들 준비 완

def get_session():
    with Session(engine) as session: # 세션 열기?
        yield session # yield문은 반복가능한 객체인 제너레이터를 반환함. / 세션에 뭘 넣을 때마다 사용하는 클래스인듯.

def seed_data():
    with Session(engine) as session:
        new_post = Post(user_id="구나현바보멍텅구리", question="좋아하는 게임은?")
        session.add(new_post)
        session.commit()

if __name__ == "__main__":
    create_db_and_tables()
    print("확인")

