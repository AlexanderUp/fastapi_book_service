from .schemas import AuthorSchema, BookSchema, PublisherSchema
from .book_repository import FakeBookRepository


class BookService:
    def __init__(self, repository: FakeBookRepository) -> None:
        self._repository = repository
    
    def list_books(self) -> list[BookSchema]:
        return self._repository.get_book_list()
    
    def get_book_by_id(self, book_id) -> BookSchema | None:
        return self._repository.get_book_by_id(book_id)
    
    def add_book(self, book) -> BookSchema:
        return self._repository.add_book(book)

    def book_count(self) -> int:
        return self._repository.book_count()
    
    def list_authors(self) -> list[AuthorSchema]:
        return self._repository.get_author_list()

    def add_author(self, author: AuthorSchema) -> AuthorSchema:
        return self._repository.add_author(author)

    def list_publishers(self) -> list[PublisherSchema]:
        return self._repository.get_publisher_list()

    def add_publisher(self, publisher: PublisherSchema) -> PublisherSchema:
        return self._repository.add_publisher(publisher)
