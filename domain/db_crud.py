from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from .db_tables import Author, Book, Publisher
from .schemas import AuthorSchema, BookSchema, PublisherSchema

DB_table_type = Author | Book | Publisher
Schema_type = AuthorSchema | BookSchema | PublisherSchema


def add_instance(
    session: Session,
    instance_schema: Schema_type,
    instance_db_table_class: DB_table_type,
) -> DB_table_type:
    instance_db = instance_db_table_class(**instance_schema.model_dump())
    session.add(instance_db)
    session.commit()
    session.refresh(instance_db)
    return instance_db


def get_instance_list_list(
    session: Session,
    instance_db_table_class: DB_table_type,
) -> list[DB_table_type]:
    return session.scalars(select(instance_db_table_class))


def get_instance_by_id(
    session: Session,
    instance_id: UUID,
    instance_db_table_class: DB_table_type,
) -> DB_table_type:
    return session.get(instance_db_table_class, instance_id)


def remove_instance_by_id(
    session: Session,
    instance_id: UUID,
    instance_db_table_class: DB_table_type,
) -> None:
    instance_db = session.get(instance_db_table_class, instance_id)
    if instance_db:
        session.delete(instance_db)
        session.commit()