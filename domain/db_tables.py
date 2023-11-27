from uuid import UUID

import sqlalchemy as sa

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Author(Base):
    __tablename__ = 'authors'

    id: Mapped[UUID] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(sa.String(50))
    books: Mapped[list['Book']] = relationship(
        back_populates='author', cascade='all, delete-orphan'
    )

    def __repr__(self) -> str:
        return f'Author(id={self.id}, name={self.name})'


class Book(Base):
    __tablename__ = 'books'

    id: Mapped[UUID] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(sa.String(50))

    author_id: Mapped[UUID] = mapped_column(sa.ForeignKey('authors.id', ondelete='CASCADE'))
    author: Mapped['Author'] = relationship(back_populates='books')

    publisher_id: Mapped[UUID] = mapped_column(sa.ForeignKey('publishers.id', ondelete='CASCADE'))
    publisher: Mapped['Publisher'] = relationship(back_populates='books')

    def __repr__(self) -> str:
        return f'Book(id={self.id}, name={self.name})'
    

class Publisher(Base):
    __tablename__ = 'publishers'

    id: Mapped[UUID] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(sa.String(50))

    books: Mapped[list['Book']] = relationship(
        back_populates='publisher', cascade='all, delete-orphan'
    )

    def __repr__(self) -> str:
        return f'Publisher(id={self.id}, name={self.name})'
