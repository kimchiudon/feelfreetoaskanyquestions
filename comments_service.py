import uuid
from typing import List
from sqlmodel import Session, select
from models import Comment

def get_comments_by_post_id(post_id: uuid.UUID, session: Session) -> List[Comment]:
    """주어진 게시물 ID에 대한 모든 댓글을 찾아 생성 시간을 기준으로 오름차순으로 정렬한다."""
    statement = select(Comment).where(Comment.post_id == post_id).order_by(Comment.created_at)
    comments = session.exec(statement).all()
    return comments


def create_comment(content: str, user_id: uuid.UUID, post_id: uuid.UUID, session: Session) -> Comment:
    """새 댓글을 생성함"""
    new_comment = Comment(content=content, user_id=user_id, post_id=post_id)
    session.add(new_comment)
    session.commit()
    session.refresh(new_comment)
    return new_comment