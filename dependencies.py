from database import SessionLocal
from domain.book_service import BookService
from domain.book_repository import SQLBookRepository


def get_service():
    session = SessionLocal()
    book_repository = SQLBookRepository(session)
    book_service = BookService(book_repository)
    
    try:
        yield book_service
    finally:
        session.close()


def get_db_session():
    session = SessionLocal()
    
    try:
        yield session
    finally:
        session.close()