from fastapi import APIRouter, Depends

from dependencies import get_book_service
from domain.book_service import BookService
from domain.schemas import PublisherSchema

router = APIRouter(
    prefix='/publishers',
    tags=['publishers'],
    responses={404: {'description': 'Not found'}},
)


@router.get('/', response_model=list[PublisherSchema])
async def list_publishers(book_service: BookService = Depends(get_book_service)):
    return book_service.list_publishers()


@router.post('/', response_model=PublisherSchema)
async def add_publisher(
    publisher: PublisherSchema, book_service: BookService = Depends(get_book_service),
):
    return book_service.add_publisher(publisher)
