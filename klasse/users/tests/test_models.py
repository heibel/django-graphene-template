from klasse.users.models import User


def test_user_unicode():
    user = User(first_name='John', last_name='Doe', email='user@example.com', password='password')

    assert user.__unicode__() == 'John Doe'
