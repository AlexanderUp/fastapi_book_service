from auth.auth_service import UserService
from auth.user_repository import SQLAlchemyUserRepository
from database import SessionLocal
from domain.book_service import BookService
from domain.book_repository import SQLAlchemyBookRepository


def get_user_service():
    session = SessionLocal()
    user_repository = SQLAlchemyUserRepository(session)
    user_service = UserService(user_repository)

    try:
        yield user_service
    finally:
        session.close()


def get_book_service():
    session = SessionLocal()
    book_repository = SQLAlchemyBookRepository(session)
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