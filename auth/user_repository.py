from abc import ABC, abstractmethod
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from .auth_db_tables import UserDB
from .auth_password_utils import get_password_hash
from .auth_schemas import UserSchemaCreate, UserSchemaInputUpdate


class AbstractUserRepository(ABC):

    @abstractmethod
    def add_user(self, user_schema: UserSchemaCreate) -> UserDB:
        pass

    @abstractmethod
    def list_users(self) -> list[UserDB]:
        pass

    @abstractmethod
    def get_user_by_id(self, user_id: UUID) -> UserDB | None:
        pass

    @abstractmethod
    def update_user_by_id(
        self, user_id: UUID, user_input_schema: UserSchemaInputUpdate,
    ) -> UserDB | None:
        pass

    @abstractmethod
    def delete_user_by_id(self, user_id: UUID) -> None:
        pass


class SQLAlchemyUserRepository(AbstractUserRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def add_user(self, user_schema: UserSchemaCreate) -> UserDB:
        password_hash = get_password_hash(user_schema.password)
        user = UserDB(
            id=user_schema.id,
            username=user_schema.username,
            email=user_schema.email,
            first_name=user_schema.first_name,
            last_name=user_schema.last_name,
            password_hash=password_hash,
        )
        self._session.add(user)
        self._session.commit()
        self._session.refresh(user)
        return user
    
    def list_users(self) -> list[UserDB]:
        return self._session.scalars(select(UserDB))
    
    def get_user_by_id(self, user_id: UUID) -> UserDB | None:
        return self._session.get(UserDB, user_id)
    
    def update_user_by_id(
        self, user_id: UUID, user_input_schema: UserSchemaInputUpdate,
    ) -> UserDB | None:
        user_db = self._session.get(UserDB, user_id)
        if not user_db:
            return None
        
        user_data_dict = user_input_schema.model_dump(exclude_unset=True)

        for key, value in user_data_dict.items():
            setattr(user_db, key, value)

        self._session.add(user_db)
        self._session.commit()
        self._session.refresh(user_db)
        return user_db
    
    def delete_user_by_id(self, user_id: UUID) -> None:
        user = self.get_user_by_id(user_id)
        if user:
            self._session.delete(user)
            self._session.commit()