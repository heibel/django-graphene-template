import pytest

from config.schema import schema as graphql_schema


@pytest.fixture(scope='session')
def schema():
    return graphql_schema


@pytest.fixture
def request_with_session(rf):
    from django.contrib.sessions.middleware import SessionMiddleware

    request = rf.request()

    middleware = SessionMiddleware()
    middleware.process_request(request)

    request.session.save()

    return request


@pytest.fixture
@pytest.mark.django_db
def user(django_user_model):
    return django_user_model.objects.create_user(
        first_name='John',
        last_name='Doe',
        email='user@example.com',
        password='password',
    )
