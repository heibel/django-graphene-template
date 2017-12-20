import pytest

from config.schema import schema as graphql_schema
from klasse.users.utils import jwt_encode_handler, jwt_payload_handler


@pytest.fixture(scope='session')
def schema():
    return graphql_schema


@pytest.fixture
@pytest.mark.django_db
def user(django_user_model):
    return django_user_model.objects.create_user(
        first_name='John',
        last_name='Doe',
        email='user@example.com',
        password='password',
    )


@pytest.fixture
def token(user):
    payload = jwt_payload_handler(user)
    jwt_token = jwt_encode_handler(payload)

    return 'Bearer {}'.format(jwt_token)
