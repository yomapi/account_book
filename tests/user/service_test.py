from random import randrange
import pytest
from django.conf import settings
from user.services import user_service


def _create_random_email() -> str:
    rand_int = randrange(1000)
    return f"{rand_int}@test.com"


@pytest.fixture(scope="session")
def django_db_setup():
    settings.DATABASES


@pytest.mark.django_db()
def test_sign_up():
    sut = user_service.sign_up(email=_create_random_email(), password="test1234!")
    assert isinstance(sut, dict)


@pytest.mark.django_db()
def test_login():
    random_email = _create_random_email()
    user_service.sign_up(email=random_email, password="test1234!")
    sut = user_service.login(email=random_email, password="test1234!")
    assert isinstance(sut, dict)
