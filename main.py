import uuid
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Depends, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from database import create_db_and_tables, get_session
from models import Post
import auth_service
from auth_dependcies import login_required, get_user_from_session # 종속성 가져오기
import comments_service
from starlette.middleware.sessions import SessionMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating tables..")
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan) #FastAPI는 클래스(Class), app은 그 클래스로부터 찍어낸 인스턴스임, app 객체는 앞으로 들어올 모든 요청을 처리함.
app.add_middleware(SessionMiddleware, secret_key="change-me-to-a-long-random-string")

app.mount("/static", StaticFiles(directory="css"), name="static")

templates = Jinja2Templates(directory="templates") 

@app.get("/", response_class=HTMLResponse)
def root():

    return RedirectResponse(url="/posts", status_code=302)

@app.get("/posts", response_class=HTMLResponse)
def get_all_posts(request: Request, session: Session = Depends(get_session)):
    
    statement = select(Post).order_by(Post.created_at.desc())
    posts = session.exec(statement).all()
    return templates.TemplateResponse("index.html", {"request": request, "posts": posts})

@app.get("/posts/new", response_class=HTMLResponse)
def new_post_form(request: Request):
    
    return templates.TemplateResponse("new-post.html",{"request": request, "post": None})

@app.post("/posts")
def create_post(
    question: str = Form(...),
    session: Session = Depends(get_session)
) : 
    
    new_post = Post(
        
        user_id = "guest",
        question=question,
        answer=None
    )

    session.add(new_post)
    session.commit()
    session.refresh(new_post)
    return RedirectResponse(url=f"/posts/{new_post.id}", status_code = 302)

@app.get("/posts/{post_id}", response_class=HTMLResponse)
def get_post_by_id(
    request: Request, 
    post_id: uuid.UUID, 
    session: Session = Depends(get_session),
    user: dict | None = Depends(get_user_from_session)
):     
    post = session.get(Post, post_id)
    comments = comments_service.get_comments_by_post_id(post_id, session)
    
    return templates.TemplateResponse(
        "post.html", 
        {
            "request": request, 
            "post": post, 
            "title": post.question,
            "user": user,
            "comments" : comments
        
        }
    )

@app.get("/auth/login", response_class=HTMLResponse)
def show_login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "title" : "Login"})

@app.post("/auth/login")
def login(
    request: Request, # 세션에 액세스하기 위해 Request 객체 주입
    username: str = Form(...),
    password: str = Form(...),
    session: Session = Depends(get_session)
):
    user = auth_service.validate_user(username, password, session)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    
    request.session["user"] = {"username": user.username, "id": str(user.id)}
    
    return RedirectResponse(url="/posts", status_code=302)

@app.get("/auth/logout")
def logout(request: Request):

    request.session.clear()
    return RedirectResponse(url="/", status_code=302)

@app.post("/posts/{post_id}/comments")
def create_comment_for_post(
    post_id: uuid.UUID,
    content: str = Form(...),
    user: dict = Depends(login_required),
    session: Session = Depends(get_session)
):
    user_id = uuid.UUID(user["id"])

    comments_service.create_comment(
        content=content, user_id=user_id, post_id=post_id, session = session        
    )

    return RedirectResponse(url=f"/posts/{post_id}", status_code=302)
