from fastapi import Depends, FastAPI

from database import SessionLocal
from domain.book_service import BookService
from domain.book_repository import SQLBookRepository
from domain.schemas import AuthorSchema, BookSchema, BookSchemaCreate, PublisherSchema

app = FastAPI()


def get_service():
    session = SessionLocal()
    book_repository = SQLBookRepository(session)
    book_service = BookService(book_repository)
    
    try:
        yield book_service
    finally:
        session.close()



@app.get('/books', response_model=list[BookSchema])
async def list_books(book_service: BookService = Depends(get_service)):
    return book_service.list_books()


@app.post('/books', response_model=BookSchema)
async def add_book(
    book: BookSchemaCreate, book_service: BookService = Depends(get_service),
):
    return book_service.add_book(book)


@app.get('/authors', response_model=list[AuthorSchema])
async def list_authors(book_service: BookService = Depends(get_service)):
    return book_service.list_authors()


@app.post('/authors', response_model=AuthorSchema)
async def add_author(
    author: AuthorSchema, book_service: BookService = Depends(get_service),
):
    return book_service.add_author(author)


@app.get('/publishers', response_model=list[PublisherSchema])
async def list_publishers(book_service: BookService = Depends(get_service)):
    return book_service.list_publishers()


@app.post('/publishers', response_model=PublisherSchema)
async def add_publisher(
    publisher: PublisherSchema, book_service: BookService = Depends(get_service),
):
    return book_service.add_publisher(publisher)
