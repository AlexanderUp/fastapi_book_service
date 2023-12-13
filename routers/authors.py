from fastapi import APIRouter, Depends

from dependencies import get_book_service
from domain.book_service import BookService
from domain.schemas import AuthorSchema

router = APIRouter(
    prefix='/authors',
    tags=['authors'],
    responses={404: {'description': 'Not found'}},
)


@router.get('/', response_model=list[AuthorSchema])
async def list_authors(book_service: BookService = Depends(get_book_service)):
    return book_service.list_authors()


@router.post('/', response_model=AuthorSchema)
async def add_author(
    author: AuthorSchema, book_service: BookService = Depends(get_book_service),
):
    return book_service.add_author(author)