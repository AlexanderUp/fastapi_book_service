from fastapi import FastAPI

from database import SessionLocal
from domain.book_service import BookService
from domain.book_repository import SQLBookRepository
from domain.schemas import AuthorSchema, BookSchema, BookSchemaCreate, PublisherSchema

app = FastAPI()

session = SessionLocal()

book_repository = SQLBookRepository(session)
book_service = BookService(book_repository)


@app.get('/books', response_model=list[BookSchema])
async def list_books():
    return book_service.list_books()


@app.post('/books', response_model=BookSchema)
async def add_book(book: BookSchemaCreate):
    return book_service.add_book(book)


@app.get('/authors', response_model=list[AuthorSchema])
async def list_authors():
    return book_service.list_authors()


@app.post('/authors', response_model=AuthorSchema)
async def add_author(author: AuthorSchema):
    return book_service.add_author(author)


@app.get('/publishers', response_model=list[PublisherSchema])
async def list_publishers():
    return book_service.list_publishers()


@app.post('/publishers', response_model=PublisherSchema)
async def add_publisher(publisher: PublisherSchema):
    return book_service.add_publisher(publisher)
