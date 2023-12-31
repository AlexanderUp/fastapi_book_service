from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .auth_schemas import TokenSchema
from .auth_dependencies import ACCESS_TOKEN_EXPIRE_MINUTES, authenticate_user, create_access_token
from dependencies import get_db_session

auth_router = APIRouter(tags=['auth'])


@auth_router.post('/token', response_model=TokenSchema)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Session = Depends(get_db_session),
):
    user = authenticate_user(session, form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={'sub': user.username}, expires_delta=access_token_expires,
    )
    return {'access_token': access_token, 'token_type': 'bearer'}
