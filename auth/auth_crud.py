from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from .auth_db_tables import UserDB
from .auth_schemas import UserSchemaCreate
from .auth_password_utils import get_password_hash


def add_user(session: Session, user_schema: UserSchemaCreate) -> UserDB:
    password_hash = get_password_hash(user_schema.password)
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


def list_users(session: Session):
    return session.scalars(select(UserDB))


def get_user_by_id(session: Session, user_id: UUID) -> UserDB:
    user = session.get(UserDB, user_id)
    return user


def remove_user_by_id(session: Session, user_id: UUID) -> None:
    user = get_user_by_id(session, user_id)
    session.delete(user)
    session.commit()


def update_user(user_input, current_user, session):
    current_user_db = session.get(UserDB, current_user.id)
    user_data_dict = user_input.model_dump(exclude_unset=True)

    for key, value in user_data_dict.items():
        setattr(current_user_db, key, value)

    session.add(current_user_db)
    session.commit()
    session.refresh(current_user_db)
    return current_user_db