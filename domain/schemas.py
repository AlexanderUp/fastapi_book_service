import uuid

from pydantic import BaseModel, ConfigDict, Field


class CommonIDNameModelSchema(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    name: str


class AuthorSchema(CommonIDNameModelSchema):
    model_config = ConfigDict(from_attributes=True)

    def __hash__(self):
        return id(self)


class BookSchema(CommonIDNameModelSchema):
    model_config = ConfigDict(from_attributes=True)

    author: AuthorSchema
    publisher: 'PublisherSchema'


class PublisherSchema(CommonIDNameModelSchema):
    model_config = ConfigDict(from_attributes=True)

    books: list[BookSchema] = Field(default=[])
