from uuid import UUID

from .schemas import AuthorSchema, BookSchema, BookSchemaCreate, PublisherSchema
from .book_repository import AbstractBookRepository


class BookService:
    def __init__(self, repository: AbstractBookRepository) -> None:
        self._repository = repository

    def add_book(self, book: BookSchemaCreate) -> BookSchema:
        return self._repository.add_book(book)
    
    def list_books(self) -> list[BookSchema]:
        return self._repository.get_book_list()
    
    def get_book_by_id(self, book_id: UUID) -> BookSchema | None:
        return self._repository.get_book_by_id(book_id)
    
    def remove_book_by_id(self, book_id: UUID) -> None:
        return self._repository.remove_book_by_id(book_id)

    def add_author(self, author: AuthorSchema) -> AuthorSchema:
        return self._repository.add_author(author)

    def list_authors(self) -> list[AuthorSchema]:
        return self._repository.get_author_list()

    def get_author_by_id(self, author_id: UUID) -> AuthorSchema:
        return self._repository.get_author_by_id(author_id)

    def remove_author_by_id(self, author_id: UUID) -> None:
        return self._repository.remove_author_by_id(author_id)
    
    def add_publisher(self, publisher: PublisherSchema) -> PublisherSchema:
        return self._repository.add_publisher(publisher)

    def list_publishers(self) -> list[PublisherSchema]:
        return self._repository.get_publisher_list()
    
    def get_publisher_by_id(self, publisher_id: UUID) -> PublisherSchema:
        return self._repository.get_publisher_by_id(publisher_id)

    def remove_publisher_by_id(self, publisher_id: UUID) -> None:
        return self._repository.remove_publisher_by_id(publisher_id)

    def book_count(self) -> int:
        return self._repository.book_count()
    
    def author_count(self) -> int:
        return self._repository.author_count()

    def publisher_count(self) -> int:
        return self._repository.publisher_count()
