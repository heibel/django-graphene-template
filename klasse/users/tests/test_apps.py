from klasse.users.apps import UsersConfig


def test_app():
    assert UsersConfig.name == 'users'
