from fastapi import FastAPI

from domain.book_service import BookService
from domain.book_repository import FakeBookRepository
from domain.schemas import AuthorSchema, BookSchema, PublisherSchema

app = FastAPI()

book_repository = FakeBookRepository()
book_service = BookService(book_repository)

orlov = AuthorSchema(name='Orlov')

road_to_ambeir = BookSchema(name='Road to Ambeir', author=orlov)
shadows_of_war = BookSchema(name='Shadows of War', author=orlov)

book_service.add_book(road_to_ambeir)
book_service.add_book(shadows_of_war)


@app.get('/books', response_model=list[BookSchema])
async def list_books():
    return book_service.list_books()


@app.post('/books', response_model=BookSchema)
async def add_book(book: BookSchema):
    return book_service.add_book(book)


@app.get('/authors', response_model=list[AuthorSchema])
async def list_authors():
    return book_service.list_authors()


@app.post('/authors', response_model=AuthorSchema)
async def add_author(author: AuthorSchema):
    return {}


@app.get('/publishers', response_model=list[PublisherSchema])
async def list_publishers():
    return {}


@app.post('/publishers', response_model=PublisherSchema)
async def add_publisher(publisher: PublisherSchema):
    return {}
