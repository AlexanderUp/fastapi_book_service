import uuid
from typing import Annotated

from pydantic import BaseModel, ConfigDict, constr, EmailStr, Field


class TokenSchema(BaseModel):
    access_token: str
    token_type: str


class TokenDataSchema(BaseModel):
    username: str | None = None


class UserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserSchemaDB(UserSchema):
    model_config = ConfigDict(from_attributes=True)

    password_hash: str


class UserSchemaCreate(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    username: constr(max_length=50)
    email: Annotated[EmailStr, Field(max_length=50)]
    first_name: constr(max_length=50) | None = None
    last_name: constr(max_length=50) | None = None
    password: str
