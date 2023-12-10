import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from auth.auth_crud import add_user, list_users, get_user_by_id, remove_user_by_id
from auth.auth_db_tables import UserDB
from auth.auth_dependencies import get_current_active_user, get_db_session, get_password_hash
from auth.auth_schemas import UserSchema, UserShemaInput, UserSchemaInputUpdate, UserSchemaCreate

router = APIRouter(
    prefix='/users',
    tags=['users'],
    responses={404: {'description': 'Not found'}},
)


@router.get('/', response_model=list[UserSchema])
async def list_users(session: Session = Depends(get_db_session)):
    return session.scalars(select(UserDB))


@router.get('/me', response_model=UserSchema)
async def read_users_me(
    current_user: Annotated[UserSchema, Depends(get_current_active_user)]
):
    return current_user


@router.put('/me', response_model=UserSchema)
async def read_users_me(
    user_input: UserSchemaInputUpdate,
    current_user: Annotated[UserSchema, Depends(get_current_active_user)],
    session: Session = Depends(get_db_session),
):
    current_user_db = session.get(UserDB, current_user.id)
    user_data_dict = user_input.model_dump(exclude_unset=True)

    for key, value in user_data_dict.items():
        setattr(current_user_db, key, value)

    session.add(current_user_db)
    session.commit()
    session.refresh(current_user_db)
    return current_user_db


@router.patch('/me', response_model=UserSchema)
async def read_users_me(
    user_input: UserSchemaInputUpdate,
    current_user: Annotated[UserSchema, Depends(get_current_active_user)],
    session: Session = Depends(get_db_session),
):
    current_user_db = session.get(UserDB, current_user.id)
    user_data_dict = user_input.model_dump(exclude_unset=True)

    for key, value in user_data_dict.items():
        setattr(current_user_db, key, value)

    session.add(current_user_db)
    session.commit()
    session.refresh(current_user_db)
    return current_user_db


@router.get('/{user_id}', response_model=UserSchema)
async def get_user_by_id(user_id: uuid.UUID, session: Session = Depends(get_db_session)):
    user = session.get(UserDB, user_id)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    return user


@router.post('/', response_model=UserSchema)
async def create_user(
    user_schema: UserSchemaCreate, session: Session = Depends(get_db_session),
):
    password_hash = get_password_hash(user_schema.password)
    user = UserDB(
        id=uuid.uuid4(),
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
async def remove_user_by_id(
    user_id: uuid.UUID, session: Session = Depends(get_db_session),
) -> None:
    user = session.get(UserDB, user_id)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    session.delete(user)
    session.commit()
