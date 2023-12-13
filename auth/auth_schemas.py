import uuid
from typing import Annotated

from pydantic import BaseModel, ConfigDict, constr, EmailStr, Field


class TokenSchema(BaseModel):
    access_token: str
    token_type: str


class TokenDataSchema(BaseModel):
    username: str | None = None


class UserSchemaInputUpdate(BaseModel):
    first_name: constr(max_length=50) | None = None
    last_name: constr(max_length=50) | None = None


class UserShemaInput(UserSchemaInputUpdate):
    username: constr(max_length=50)
    email: Annotated[EmailStr, Field(max_length=50)]


class BaseUserSchema(UserShemaInput):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)


class UserSchema(BaseUserSchema):
    model_config = ConfigDict(from_attributes=True)

    disabled: bool | None = None


class UserSchemaDB(UserSchema):
    model_config = ConfigDict(from_attributes=True)

    password_hash: str


class UserSchemaCreate(BaseUserSchema):
    password: str
