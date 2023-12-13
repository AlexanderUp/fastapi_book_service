from fastapi import APIRouter, Depends

from dependencies import get_book_service
from domain.book_service import BookService
from domain.schemas import BookSchema, BookSchemaCreate

router = APIRouter(
    prefix='/books',
    tags=['books'],
    responses={404: {'description': 'Not found'}},
)


@router.get('/', response_model=list[BookSchema])
async def list_books(book_service: BookService = Depends(get_book_service)):
    return book_service.list_books()


@router.post('/', response_model=BookSchema)
async def add_book(
    book: BookSchemaCreate, book_service: BookService = Depends(get_book_service),
):
    return book_service.add_book(book)