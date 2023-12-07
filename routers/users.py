from typing import Annotated

from fastapi import APIRouter, Depends

from auth.auth_schemas import User
from auth.auth_dependencies import get_current_active_user

router = APIRouter(
    prefix='/users',
    tags=['users'],
    responses={404: {'description': 'Not found'}},
)


@router.get('/me', response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return current_user
