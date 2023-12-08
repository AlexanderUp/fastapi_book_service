import uuid
from typing import Annotated

from pydantic import BaseModel, ConfigDict, constr, EmailStr, Field, model_validator, ValidationError


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
    password1: str
    password2: str

    @model_validator(mode='after')
    def check_password_match(self) -> 'UserSchemaCreate':
        pw1 = self.password1
        pw2 = self.password2

        if pw1 is not None and pw2 is not None and pw1 != pw2:
            raise ValidationError('Passwords do not match')
        return self
