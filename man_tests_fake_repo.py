from domain.schemas import AuthorSchema, BookSchema, PublisherSchema
from domain.book_repository import FakeBookRepository


if __name__ == '__main__':
    print('*' * 125)

    alpha = PublisherSchema(name='alpha')

    pehov = AuthorSchema(name='Pehov')
    orlov = AuthorSchema(name='Orlov')

    road_to_ambeir = BookSchema(name='Road to Ambeir', author=orlov, publisher=alpha)
    shadows_of_war = BookSchema(name='Shadows of War', author=orlov, publisher=alpha)

    sneaking_in_shadow = BookSchema(name='Sneaking in shadow', author=pehov, publisher=alpha)
    djanga_with_shadows = BookSchema(name='Djanga with shadows', author=pehov, publisher=alpha)

    repo = FakeBookRepository()
    repo.add_book(road_to_ambeir)
    repo.add_book(shadows_of_war)
    repo.add_book(sneaking_in_shadow)
    repo.add_book(djanga_with_shadows)

    for book in repo.get_book_list():
        print(book)

    book_searched = repo.get_book_by_id(road_to_ambeir.id)
    assert book_searched is road_to_ambeir

    repo.remove_book_by_id(road_to_ambeir.id)

    assert road_to_ambeir not in repo