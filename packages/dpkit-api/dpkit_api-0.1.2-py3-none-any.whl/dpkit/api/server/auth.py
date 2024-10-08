from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import HTTPBearer

from dpkit.api import User

security = HTTPBearer()


async def current_user(
    bearer: Annotated[str, Depends(security)],
    request: Request,
) -> User:
    user = request.app.state.users.get(bearer.credentials)
    if not user:
        raise HTTPException(status_code=401, detail="User is not authorized")
    return user


async def active_user(
    user: Annotated[User, Depends(current_user)],
    request: Request,
) -> User:
    if user.disabled:
        raise HTTPException(status_code=400, detail="User is disabled")
    return user


router = APIRouter()


@router.get("/me")
async def identify(
    user: Annotated[User, Depends(active_user)],
    request: Request,
) -> User:
    """
    Use this route to validate identity and credentials.
    """
    return user
