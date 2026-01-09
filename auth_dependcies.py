# auth_dependencies.py
from fastapi import Request, HTTPException, status

def login_required(request: Request) -> dict:
    user = request.session.get("user")
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Login required"
        )
    return user

def get_user_from_session(request: Request) -> dict | None:
    return request.session.get("user")
