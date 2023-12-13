import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from auth.auth_dependencies import get_current_active_user
from auth.auth_schemas import UserSchema, UserSchemaInputUpdate, UserSchemaCreate
from auth.auth_service import UserService
from dependencies import get_user_service

router = APIRouter(
    prefix='/users',
    tags=['users'],
    responses={404: {'description': 'Not found'}},
)


@router.get('/', response_model=list[UserSchema])
async def list_users(user_service: UserService = Depends(get_user_service)):
    return user_service.list_users()


@router.get('/me', response_model=UserSchema)
async def read_users_me(
    current_user: Annotated[UserSchema, Depends(get_current_active_user)]
):
    return current_user


@router.put('/me', response_model=UserSchema)
async def read_users_me(
    user_input_chema: UserSchemaInputUpdate,
    current_user: Annotated[UserSchema, Depends(get_current_active_user)],
    user_service: UserService = Depends(get_user_service),
):
    return user_service.update_user_by_id(
        user_id=current_user.id, user_input_schema=user_input_chema,
    )


@router.patch('/me', response_model=UserSchema)
async def read_users_me(
    user_input_schema: UserSchemaInputUpdate,
    current_user: Annotated[UserSchema, Depends(get_current_active_user)],
    user_service: UserService = Depends(get_user_service),
):
    return user_service.update_user_by_id(
        user_id=current_user.id, user_input_schema=user_input_schema,
    )


@router.get('/{user_id}', response_model=UserSchema)
async def get_user_by_id(user_id: uuid.UUID, user_service: UserService = Depends(get_user_service),
):
    user = user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    return user


@router.post('/', response_model=UserSchema)
async def create_user(
    user_schema: UserSchemaCreate,
    user_service: UserService = Depends(get_user_service),

):
    return user_service.add_user(user_schema)


@router.delete('/{user_id}')
async def remove_user_by_id(
    user_id: uuid.UUID, user_service: UserService = Depends(get_user_service),

) -> None:
    return user_service.delete_user_by_id(user_id)
