import pytest
from main import BooksCollector
from test_data import BOOKS_BY_GENRE


@pytest.fixture
def books_collection():
    return BooksCollector()

@pytest.fixture
def books_collection_with_one_book(books_collection):
    books_collection.add_new_book("Дюна")
    return books_collection

@pytest.fixture
def books_collection_with_genre(books_collection):

    for book, genre in BOOKS_BY_GENRE.items():
        books_collection.add_new_book(book)
        books_collection.set_book_genre(book, genre)

    return books_collection

