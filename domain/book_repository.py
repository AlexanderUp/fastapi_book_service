from abc import ABC, abstractmethod
from uuid import UUID

from sqlalchemy import func, select

from .db_tables import Author, Book, Publisher
from .schemas import AuthorSchema, BookSchema, PublisherSchema


class AbstractBookRepository(ABC):

    @abstractmethod
    def __init__(self) -> None:
        pass

    @abstractmethod
    def add_book(self, book: BookSchema) -> BookSchema:
        pass

    @abstractmethod
    def get_book_list(self) -> list[BookSchema]:
        pass

    @abstractmethod
    def get_book_by_id(self, book_id: UUID) -> BookSchema:
        pass
    
    @abstractmethod
    def remove_book_by_id(self, book_id: UUID) -> None:
        pass

    def add_author(self, author: AuthorSchema) -> AuthorSchema:
        pass

    @abstractmethod
    def get_author_list(self) -> list[AuthorSchema]:
        pass

    @abstractmethod
    def get_author_by_id(self, author_id: UUID) -> AuthorSchema:
        pass

    def remove_author_by_id(self, author_id: UUID) -> None:
        pass

    def add_publisher(self, publisher_id: UUID) -> PublisherSchema:
        pass

    def get_publisher_list(self) -> list[PublisherSchema]:
        pass

    def get_publisher_by_id(self, publisher_id: UUID) -> PublisherSchema:
        pass

    def remove_publisher_by_id(self, publisher_id: UUID) -> None:
        pass

    def book_count() -> int:
        pass

    def author_count() -> int:
        pass

    def publisher_count() -> int:
        pass


class FakeBookRepository(AbstractBookRepository):
    def __init__(self):
        self._books: list[BookSchema] = []

    def add_book(self, book: BookSchema) -> BookSchema:
        self._books.append(book)
        return book

    def get_book_list(self) -> list[BookSchema]:
        return self._books

    def get_book_by_id(self, book_id: UUID) -> BookSchema | None:
        for book in self._books:
            if book.id == book_id:
                return book
        return None
    
    def remove_book_by_id(self, book_id: UUID) -> None:
        for book in self._books:
            if book.id == book_id:
                self._books.remove(book)
                break
        return None

    def get_author_list(self) -> list[AuthorSchema]:
        return {book.author for book in self._books}

    def get_author_by_id(self, author_id: UUID) -> AuthorSchema | None:
        for author in self.get_author_list():
            if author.id == author_id:
                return author
        return None

    def book_count(self) -> int:
        return len(self._books)

    def __contains__(self, book):
        return book in self._books


class SQLBookRepository(AbstractBookRepository):

    def __init__(self, session) -> None:
        self._session = session

    def add_book(self, book: BookSchema) -> Book:
        book_db: Book = Book(**book.model_dump())
        self._session.add(book_db)
        self._session.commit()
        return book_db

    def get_book_list(self) -> list[Book]:
        return self._session.scalars(select(Book))

    def get_book_by_id(self, book_id: UUID) -> Book | None:
        return self._session.get(Book, book_id)
    
    def remove_book_by_id(self, book_id: UUID) -> None:
        book_db: Book | None = self._session.get(Book, book_id)
        if book_db:
            self._session.delete(book_db)
            self._session.commit()

    def add_author(self, author: AuthorSchema) -> Author:
        author_db: Author = Author(**author.model_dump())
        self._session.add(author_db)
        self._session.commit()
        return author_db

    def get_author_list(self) -> list[Author]:
        return self._session.scalars(select(Author))

    def get_author_by_id(self, author_id: UUID) -> Author | None:
        return self._session.get(Author, author_id)

    def remove_author_by_id(self, author_id: UUID) -> None:
        author_db: Author | None = self._session.get(Author, author_id)
        if author_db:
            self._session.delete(author_db)
            self._session.commit()

    def add_publisher(self, publisher: PublisherSchema) -> Publisher:
        publisher_db: Publisher = Publisher(**publisher.model_dump())
        self._session.add(publisher_db)
        self._session.commit()
        return publisher_db

    def get_publisher_list(self) -> list[Publisher]:
        return self._session.scalars(select(Publisher))

    def get_publisher_by_id(self, publisher_id: UUID) -> Publisher | None:
        return self._session.get(Publisher, publisher_id)

    def remove_publisher_by_id(self, publisher_id: UUID) -> None:
        publisher_db: Publisher | None = self._session.get(Publisher, publisher_id)
        if publisher_db:
            self._session.delete(publisher_db)
            self._session.commit()

    def author_count(self) -> int:
        return self._session.scalar(select(func.count('*')).select_from(Author))

    def book_count(self) -> int:
        return self._session.scalar(select(func.count('*')).select_from(Book))

    def publisher_count(self) -> int:
        return self._session.scalar(select(func.count('*')).select_from(Publisher))
