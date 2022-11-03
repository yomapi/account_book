import pytest
from django.conf import settings
from user.services import user_service


@pytest.fixture(scope="session")
def django_db_setup():
    settings.DATABASES


@pytest.mark.django_db()
def test_sign_up():
    sut = user_service.sign_up(email="test@test.com", password="test1234!")
    assert isinstance(sut, dict)


@pytest.mark.django_db()
def test_login():
    sut = user_service.login(email="test@test.com", password="test1234!")
    assert isinstance(sut, dict)
