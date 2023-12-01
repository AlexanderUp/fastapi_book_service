import sqlalchemy as sa
from sqlalchemy.orm import Session

from domain.book_repository import SQLBookRepository
from domain.db_tables import Base
from domain.schemas import AuthorSchema, BookSchemaCreate, PublisherSchema


if __name__ == '__main__':
    print('*' * 125)

    engine = sa.create_engine(f'sqlite://', echo=True)
    
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        repo = SQLBookRepository(session)

        orlov = AuthorSchema(name='Orlov')
        pehov = AuthorSchema(name='Pehov')
        alpha_pub = PublisherSchema(name='alpha')

        orlov_db = repo.add_author(orlov)
        pehov_db = repo.add_author(pehov)
        alpha_db = repo.add_publisher(alpha_pub)

        author_count = repo.author_count()
        assert author_count == 2

        publisher_count = repo.publisher_count()
        assert publisher_count == 1

        road_to_ambeir = BookSchemaCreate(name='Road to Ambeir', author_id=orlov_db.id, publisher_id=alpha_db.id)
        shadows_of_war = BookSchemaCreate(name='Shadows of War', author_id=orlov_db.id, publisher_id=alpha_db.id)

        sneaking_in_shadow = BookSchemaCreate(name='Sneaking in shadow', author_id=pehov_db.id, publisher_id=alpha_db.id)
        djanga_with_shadows = BookSchemaCreate(name='Djanga with shadows', author_id=pehov_db.id, publisher_id=alpha_db.id)

        repo.add_book(road_to_ambeir)
        repo.add_book(shadows_of_war)
        repo.add_book(sneaking_in_shadow)
        repo.add_book(djanga_with_shadows)

        book_count = repo.book_count()
        assert book_count == 4

        repo.remove_author_by_id(orlov_db.id)
        repo.remove_author_by_id(pehov_db.id)

        assert repo.author_count() == 0
        assert repo.book_count() == 0

        assert repo.publisher_count() == 1

        repo.remove_publisher_by_id(alpha_db.id)
        assert repo.publisher_count() == 0
