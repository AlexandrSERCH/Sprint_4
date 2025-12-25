import pytest
from main import BooksCollector


class TestBooksCollector:

    @pytest.fixture
    def books_collection(self):
        return BooksCollector()

    @pytest.fixture
    def books_collection_with_one_book(self, books_collection):
        books_collection.add_new_book("Дюна")
        return books_collection

    @pytest.fixture
    def books_collection_with_genre(self, books_collection):
        books_by_genre = {
            "Дюна": "Фантастика",
            "Основание": "Фантастика",
            "Оно": "Ужасы",
            "Зов Ктулху": "Ужасы",
            "Убийство в «Восточном экспрессе»": "Детективы",
            "Собака Баскервилей": "Детективы",
            "Холодное сердце. История Анны и Эльзы": "Мультфильмы",
            "Король Лев. Официальная новеллизация": "Мультфильмы",
            "Трое в лодке, не считая собаки": "Комедии",
            "Похождения бравого солдата Швейка": "Комедии"
        }

        for book, genre in books_by_genre.items():
            books_collection.add_new_book(book)
            books_collection.set_book_genre(book, genre)

        return books_collection

    @pytest.mark.parametrize("title_book", ['Ю', 'Алиса в стране чудес'])
    def test_add_new_book_valid_book_returns_created_book(self, books_collection, title_book):
        books_collection.add_new_book(title_book)
        assert books_collection.get_books_genre().get(title_book) is not None

    def test_add_new_book_with_duplicate_book_returns_one_book(self, books_collection_with_one_book):
        books_collection_with_one_book.add_new_book("Дюна")
        assert len(books_collection_with_one_book.get_books_genre()) == 1

    @pytest.mark.parametrize("title_book",["", "Название книги, которая содержит 41 симв."])
    def test_add_new_book_with_0_or_41_char_title_returns_empty_dict(self, books_collection, title_book):
        books_collection.add_new_book(title_book)
        assert len(books_collection.get_books_genre()) == 0

    def test_set_book_genre_valid_genre_returns_book_with_genre(self, books_collection_with_one_book):
        book = "Дюна"
        genre = "Фантастика"
        books_collection_with_one_book.set_book_genre(book, genre)
        assert books_collection_with_one_book.get_book_genre(book) == genre

    def test_set_book_genre_non_existent_book_returns_unchanged_books_genre(self, books_collection):
        book = "Книга, которой нет"
        books_collection.set_book_genre(book, "Фантастика")
        assert books_collection.get_book_genre(book) is None

    def test_set_book_genre_non_existent_genre_returns_unchanged_books_genre(self, books_collection_with_one_book):
        existing_book = "Дюна"
        genre = "Жанр, которого нет"
        books_collection_with_one_book.set_book_genre(existing_book, genre)
        assert books_collection_with_one_book.get_book_genre(existing_book) == ''

    def test_get_book_genre_exist_books_returns_comedy_genre(self, books_collection_with_genre):
        assert books_collection_with_genre.get_book_genre("Похождения бравого солдата Швейка") == "Комедии"

    def test_get_book_genre_non_existent_book_returns_None(self, books_collection):
        book = "Книга, которой нет"
        assert books_collection.get_book_genre(book) is None

    def test_get_books_with_specific_genre_exist_genre_returns_books_of_given_genre(self, books_collection_with_genre):
        expected_result = ['Оно', 'Зов Ктулху']
        actual_result = books_collection_with_genre.get_books_with_specific_genre("Ужасы")
        assert actual_result == expected_result

    def test_get_books_with_specific_genre_when_no_books_returns_empty_list(self, books_collection):
        assert books_collection.get_books_with_specific_genre("Мультфильмы") == []

    def test_get_books_with_specific_genre_non_exist_genre_returns_empty_list(self, books_collection_with_genre):
        assert books_collection_with_genre.get_books_with_specific_genre("Аниме") == []

    def test_get_books_genre_books_with_genre_returned_list_books_with_genre(self, books_collection):
        book = "Дюна"
        genre = "Фантастика"

        books_collection.add_new_book(book)
        books_collection.set_book_genre(book, genre)
        actual_result = books_collection.get_books_genre()

        assert len(actual_result) == 1
        assert actual_result[book] == genre

    def test_get_books_for_children_books_have_genre_age_rating_returns_filtered_book_list(self, books_collection_with_genre):
        actual_result = books_collection_with_genre.get_books_for_children()

        books_having_age_rating = []
        for book, genre in books_collection_with_genre.books_genre.items():
            for genre_age_rating in books_collection_with_genre.genre_age_rating:
                if genre == genre_age_rating:
                    books_having_age_rating.append(book)

        assert all(book not in books_having_age_rating for book in actual_result)

    def test_add_book_in_favorites_valid_book_returns_favourites_list(self, books_collection_with_genre):
        book_in_collection = list(books_collection_with_genre.get_books_genre())[0]
        books_collection_with_genre.add_book_in_favorites(book_in_collection)
        actual_result = books_collection_with_genre.get_list_of_favorites_books()[0]

        assert book_in_collection == actual_result

    def test_add_book_in_favorites_duplicate_book_returns_unchanged_favourites_list(self, books_collection_with_genre):
        book_in_collection = list(books_collection_with_genre.get_books_genre())[0]
        books_collection_with_genre.add_book_in_favorites(book_in_collection)
        books_collection_with_genre.add_book_in_favorites(book_in_collection)
        actual_result = books_collection_with_genre.get_list_of_favorites_books()

        assert len(actual_result) == 1

    def test_delete_book_from_favorites_book_in_favorites_returns_list_without_book(self, books_collection_with_genre):
        book_in_collection = list(books_collection_with_genre.get_books_genre())[0]
        books_collection_with_genre.add_book_in_favorites(book_in_collection)
        books_collection_with_genre.delete_book_from_favorites(book_in_collection)
        actual_result = books_collection_with_genre.get_list_of_favorites_books()

        assert actual_result == []

    def test_get_list_of_favorites_books_valid_book_returns_favourites_list(self, books_collection_with_genre):
        book_1 = list(books_collection_with_genre.get_books_genre())[0]
        book_2 = list(books_collection_with_genre.get_books_genre())[1]

        books_collection_with_genre.add_book_in_favorites(book_1)
        books_collection_with_genre.add_book_in_favorites(book_2)

        actual_result = books_collection_with_genre.get_list_of_favorites_books()

        assert len(actual_result) == 2