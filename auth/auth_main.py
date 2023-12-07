from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from .auth_schemas import UserInDB
from .auth_db_tables import fake_users_db
from .auth_dependencies import fake_hash_password

auth_router = APIRouter(
    tags=['auth'],
)


@auth_router.post('/token')
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail='Incorrect username or password')
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail='Incorrect username or password')
    
    return {'access_token': user.username, 'token_type': 'bearer'}
