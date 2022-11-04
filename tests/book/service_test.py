import pytest
from django.conf import settings
from book.services import book_service
from exceptions import NoPermissionError
from rest_framework.exceptions import ValidationError
from book.models import Book


@pytest.fixture(scope="session")
def django_db_setup():
    settings.DATABASES


invalid_book_data = [
    ({"amount": 13, "user": -1, "memo": "something_memo"}, ValidationError),
    ({"amount": -1, "user": 1, "memo": "something_memo"}, ValidationError),
]

invalid_book_update_data = [
    ({"amount": 13, "user": 5, "memo": "something_memo"}, NoPermissionError),
    ({"amount": -1, "user": 1, "memo": "something_memo"}, ValidationError),
]


@pytest.mark.django_db()
def test_craete_book():
    sut = book_service.create({"user": 1, "amount": 1000, "memo": "this is memo"})
    assert isinstance(sut, dict)


@pytest.mark.django_db()
@pytest.mark.parametrize("test_input, exception", invalid_book_data)
def test_craete_book_with_invalid_data(test_input, exception):
    with pytest.raises(exception):
        sut = book_service.create(test_input)


@pytest.mark.django_db()
def test_get_book():
    book = book_service.create({"amount": 1500, "user": 1, "memo": "something_memo"})
    sut = book_service.get(book["id"], 1)
    assert isinstance(sut, dict)


@pytest.mark.django_db()
def test_get_book_with_invalid_user_id():
    book = book_service.create({"amount": 1500, "user": 1, "memo": "something_memo"})
    with pytest.raises(NoPermissionError):
        book_service.get(book["id"], 5)


@pytest.mark.django_db()
def test_get_book_with_invalid_user_id():
    book = book_service.create({"amount": 1500, "user": 1, "memo": "something_memo"})
    with pytest.raises(NoPermissionError):
        book_service.get(book["id"], 5)


@pytest.mark.django_db()
def test_update_book():
    book = book_service.create({"amount": 1500, "user": 1, "memo": "something_memo"})
    sut = book_service.update(book["id"], 1, {"amount": 1200, "memo": "updated"})
    assert sut["amount"] == 1200
    assert sut["memo"] == "updated"


@pytest.mark.django_db()
@pytest.mark.parametrize("test_input, exception", invalid_book_update_data)
def test_update_with_invalid_data(test_input, exception):
    book = book_service.create({"amount": 1500, "user": 1, "memo": "something_memo"})
    with pytest.raises(exception):
        book_service.update(book["id"], test_input["user"], test_input)


@pytest.mark.django_db()
def test_delete():
    book = book_service.create({"amount": 1500, "user": 1, "memo": "something_memo"})
    sut = book_service.delete(book["id"], 1)
    assert sut
    with pytest.raises(Book.DoesNotExist):
        book_service.get(book["id"], 1)


@pytest.mark.django_db()
def test_delete_with_invalid_user():
    book = book_service.create({"amount": 1500, "user": 1, "memo": "something_memo"})
    with pytest.raises(NoPermissionError):
        book_service.delete(book["id"], 2)


@pytest.mark.django_db()
def test_recover():
    book = book_service.create({"amount": 1500, "user": 1, "memo": "something_memo"})
    book_service.delete(book["id"], 1)
    sut = book_service.recover(book["id"], 1)
    assert sut["deleted_at"] == None


@pytest.mark.django_db()
def test_recover_with_not_deleted_book():
    book = book_service.create({"amount": 1500, "user": 1, "memo": "something_memo"})
    with pytest.raises(Book.DoesNotExist):
        book_service.recover(book["id"], 1)
