from uuid import UUID

from .auth_db_tables import UserDB
from .auth_schemas import UserSchemaCreate, UserSchemaInputUpdate
from .user_repository import AbstractUserRepository


class UserService:
    def __init__(self, repository: AbstractUserRepository) -> None:
        self._repository = repository

    def add_user(self, user_schema: UserSchemaCreate) -> UserDB:
        return self._repository.add_user(user_schema)
    
    def list_users(self) -> list[UserDB]:
        return self._repository.list_users()
    
    def get_user_by_id(self, user_id: UUID) -> UserDB | None:
        return self._repository.get_user_by_id(user_id)

    def update_user_by_id(
        self, user_id: UUID, user_input_schema: UserSchemaInputUpdate,
    ) -> UserDB | None:
        return self._repository.update_user_by_id(user_id, user_input_schema)
    
    def delete_user_by_id(self, user_id: UUID) -> None:
        return self._repository.delete_user_by_id(user_id)