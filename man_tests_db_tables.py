from uuid import uuid4

import sqlalchemy as sa
from sqlalchemy.orm import Session, selectinload, joinedload

from domain.db_tables import Author, Base, Book, Publisher
from domain.schemas import AuthorSchema, PublisherSchema


if __name__ == '__main__':
    print('*' * 125)

    engine = sa.create_engine(f'sqlite://', echo=True)
    
    Base.metadata.create_all(engine)

    with Session(engine) as session:

        orlov = AuthorSchema(name='Orlov')
        pehov = AuthorSchema(name='Pehov')
        alpha_pub = PublisherSchema(name='alpha')

        print(type(orlov), orlov)
        print(type(pehov), pehov)
        print(type(alpha_pub), alpha_pub)

        orlov_db = Author(**orlov.model_dump())
        pehov_db = Author(**pehov.model_dump())
        alpha_pub_db = Publisher(**alpha_pub.model_dump())

        print(type(orlov_db), orlov_db)
        print(type(pehov_db), pehov_db)
        print(type(alpha_pub_db), alpha_pub_db)
        
        session.add_all([orlov_db, pehov_db, alpha_pub_db])
        session.commit()
        
        session.refresh(orlov_db)
        session.refresh(pehov_db)
        session.refresh(alpha_pub_db)

        print(orlov_db)
        print(pehov_db)
        print(alpha_pub_db)

        road_to_ambeir = Book(id=uuid4(), name='Road to Ambeir', author=orlov_db, publisher=alpha_pub_db)
        shadows_of_war = Book(id=uuid4(), name='Shadows of War', author=orlov_db, publisher=alpha_pub_db)

        sneaking_in_shadow = Book(id=uuid4(), name='Sneaking in shadow', author=pehov_db, publisher=alpha_pub_db)
        djanga_with_shadows = Book(id=uuid4(), name='Djanga with shadows', author=pehov_db, publisher=alpha_pub_db)

        session.add_all(
            [
                road_to_ambeir,
                shadows_of_war,
                sneaking_in_shadow,
                djanga_with_shadows,
            ],
        )
        session.commit()

        print('=' * 125)

        for book in session.scalars(sa.select(Book).options(joinedload(Book.author), joinedload(Book.publisher))):
            print('^^^^^^^^ loading book....')
            print(book, book.name)
            print(book.author, book.author.name)
            print(book.publisher, book.publisher.name)

        print('+' * 125)

        for author in session.scalars(sa.select(Author).options(joinedload(Author.books))).unique():
            print('++++++++ loading book....')
            print(author.books)

        session.delete(orlov_db)
        session.commit()

        print('&' * 125)

        for author in session.scalars(sa.select(Author).options(selectinload(Author.books))):
            print('&&&&&&&& loading book....')
            print(author.name)

        for book in session.scalars(sa.select(Book)):
            print('+++&&+++ loading book....')
            print(book)