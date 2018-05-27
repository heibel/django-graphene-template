import pytest

from django.contrib.auth import get_user_model


@pytest.mark.django_db
def test_create_user():
    try:
        get_user_model().objects.create_user(
            email="user@example.com", password="password"
        )
    except Exception as e:
        pytest.fail(e)


@pytest.mark.django_db
def test_create_user_error():
    with pytest.raises(ValueError):
        get_user_model().objects.create_user(username="jdoe", password="password")


@pytest.mark.django_db
def test_create_superuser():
    try:
        get_user_model().objects.create_superuser(
            email="user@example.com", password="password"
        )
    except Exception as e:
        pytest.fail(e)


@pytest.mark.django_db
def test_create_superuser_staff_error():
    with pytest.raises(ValueError, message="Superuser must have is_staff=True"):
        get_user_model().objects.create_superuser(
            email="user@example.com", password="password", is_staff=False
        )


@pytest.mark.django_db
def test_create_superuser_superuser_error():
    with pytest.raises(ValueError, message="Superuser must have is_superuser=True"):
        get_user_model().objects.create_superuser(
            email="user@example.com", password="password", is_superuser=False
        )
