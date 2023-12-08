from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from auth.auth_crud import add_user, list_users, get_user_by_id, remove_user_by_id
from auth.auth_db_tables import UserDB
from auth.auth_dependencies import get_current_active_user, get_db_session, get_password_hash
from auth.auth_schemas import UserSchema, UserSchemaCreate

router = APIRouter(
    prefix='/users',
    tags=['users'],
    responses={404: {'description': 'Not found'}},
)


@router.get('/', response_model=list[UserSchema])
async def list_users(session: Session = Depends(get_db_session)):
    return session.scalars(select(UserDB))


@router.get('/{user_id}', response_model=UserSchema)
async def get_user_by_id(user_id: UUID, session: Session = Depends(get_db_session)):
    user = session.get(UserDB, user_id)
    return user


@router.post('/', response_model=UserSchema)
async def create_user(
    user_schema: UserSchemaCreate, session: Session = Depends(get_db_session),
):
    password_hash = get_password_hash(user_schema.password1)
    user = UserDB(
        id=user_schema.id,
        username=user_schema.username,
        email=user_schema.email,
        first_name=user_schema.first_name,
        last_name=user_schema.last_name,
        password_hash=password_hash,
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.delete('/{user_id}')
async def remove_user_by_id(user_id: UUID, session: Session = Depends(get_db_session)) -> None:
    user = session.get(UserDB, user_id)
    session.delete(user)
    session.commit()


@router.get('/me', response_model=UserSchema)
async def read_users_me(
    current_user: Annotated[UserSchema, Depends(get_current_active_user)]
):
    return current_user
