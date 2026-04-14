from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Annotated
from ..services.auth_services import authenticate_user, get_current_user
from ...auth.utils.auth_utils import create_access_token, create_refresh_token
from fastapi.security import OAuth2PasswordRequestForm
from ..models import Token
from ...database import get_db
from ...models import User


router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)

@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
) -> Token:
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)
    return Token(
        access_token=access_token,
        refresh_token=refresh_token)

@router.get("/me")
def me(user: User = Depends(get_current_user)):
    return user