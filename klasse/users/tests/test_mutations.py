from unittest import mock

import pytest

from django.core import signing

from klasse.users.utils import generate_activation_token


@pytest.mark.django_db
def test_register_mutation_success(schema, mailoutbox):
    query = '''
        mutation Register($email: String!, $password: String!, $name: String!) {
            register(email: $email, password: $password, name: $name) {
                success
                errors
            }
        }
    '''

    variables = {'email': 'user@example.com', 'password': 'password', 'name': 'John Doe'}

    expected = {
        'register': {
            'success': True,
            'errors': None,
        },
    }

    result = schema.execute(query, variable_values=variables)

    assert not result.errors
    assert result.data == expected
    assert len(mailoutbox) == 1


@pytest.mark.django_db
def test_register_mutation_error(schema):
    query = '''
        mutation Register($email: String!, $password: String!, $name: String!) {
            register(email: $email, password: $password, name: $name) {
                success
                errors
            }
        }
    '''

    variables = {'email': 'user@example.com', 'password': 'password', 'name': 'John Doe'}

    expected = {
        'register': {
            'success': False,
            'errors': ['Email already registered.'],
        },
    }

    schema.execute(query, variable_values=variables)

    result = schema.execute(query, variable_values=variables)

    assert not result.errors
    assert result.data == expected


@pytest.mark.django_db
def test_register_snapshot(schema, snapshot, mailoutbox):
    query = '''
        mutation Register($email: String!, $password: String!, $name: String!) {
            register(email: $email, password: $password, name: $name) {
                success
                errors
            }
        }
    '''

    variables = {'email': 'user@example.com', 'password': 'password', 'name': 'John Doe'}

    result = schema.execute(query, variable_values=variables)

    snapshot.assert_match(result.data)
    snapshot.assert_match(mailoutbox[0].subject)


@pytest.mark.django_db
def test_activate_mutation_success(schema, user, mailoutbox):
    activation_token = generate_activation_token(user)

    query = '''
        mutation Activate($activation_token: String!) {
            activate(activationToken: $activation_token) {
                success
                errors
            }
        }
    '''

    variables = {
        'activation_token': activation_token,
    }

    expected = {
        'activate': {
            'success': True,
            'errors': None,
        },
    }

    result = schema.execute(query, variable_values=variables)

    user.refresh_from_db()

    assert not result.errors
    assert result.data == expected

    assert user.is_active
    assert len(mailoutbox) == 1


@pytest.mark.django_db
def test_activate_mutation_user_error(schema, user):
    activation_token = generate_activation_token(user)

    query = '''
        mutation Activate($activation_token: String!) {
            activate(activationToken: $activation_token) {
                success
                errors
            }
        }
    '''

    variables = {
        'activation_token': activation_token,
    }

    expected = {
        'activate': {
            'success': False,
            'errors': ['Unknown user'],
        },
    }

    with mock.patch('klasse.users.mutations.signing.loads', return_value='unknown@example.com'):
        result = schema.execute(query, variable_values=variables)

    assert not result.errors
    assert result.data == expected


@pytest.mark.django_db
def test_activate_mutation_token_error(schema, user):
    activation_token = generate_activation_token(user)

    query = '''
        mutation Activate($activation_token: String!) {
            activate(activationToken: $activation_token) {
                success
                errors
            }
        }
    '''

    variables = {
        'activation_token': activation_token,
    }

    expected = {
        'activate': {
            'success': False,
            'errors': ['Stale token'],
        },
    }

    with mock.patch('klasse.users.mutations.signing.loads', side_effect=signing.BadSignature):
        result = schema.execute(query, variable_values=variables)

    assert not result.errors
    assert result.data == expected


@pytest.mark.django_db
def test_activate_mutation_snapshot(schema, user, mailoutbox, snapshot):
    activation_token = generate_activation_token(user)

    query = '''
        mutation Activate($activation_token: String!) {
            activate(activationToken: $activation_token) {
                success
                errors
            }
        }
    '''

    variables = {
        'activation_token': activation_token,
    }

    result = schema.execute(query, variable_values=variables)

    snapshot.assert_match(result.data)
    snapshot.assert_match(mailoutbox[0].subject)


@pytest.mark.django_db
def test_login_mutation_success(schema, user, request_with_session):
    user.is_active = True
    user.save()

    query = '''
        mutation Login($email: String!, $password: String!) {
            login(email: $email, password: $password) {
                success
                errors
            }
        }
    '''

    variables = {'email': 'user@example.com', 'password': 'password'}

    expected = {
        'login': {
            'success': True,
            'errors': None,
        },
    }

    result = schema.execute(query, context_value=request_with_session, variable_values=variables)

    assert not result.errors
    assert result.data == expected


@pytest.mark.django_db
def test_login_mutation_error(schema, request_with_session):
    query = '''
        mutation Login($email: String!, $password: String!) {
            login(email: $email, password: $password) {
                success
                errors
            }
        }
    '''

    variables = {'email': 'user@example.com', 'password': 'password'}

    expected = {
        'login': {
            'success': False,
            'errors': ['Email and/or password are unknown'],
        },
    }

    result = schema.execute(query, context_value=request_with_session, variable_values=variables)

    assert not result.errors
    assert result.data == expected


@pytest.mark.django_db
def test_login_snapshot(schema, user, snapshot, request_with_session):
    user.is_active = True
    user.save()

    query = '''
        mutation Login($email: String!, $password: String!) {
            login(email: $email, password: $password) {
                success
                errors
            }
        }
    '''

    variables = {'email': 'user@example.com', 'password': 'password'}

    result = schema.execute(query, context_value=request_with_session, variable_values=variables)

    snapshot.assert_match(result.data)


@pytest.mark.django_db
def test_logout_mutation_success(schema, request_with_session):
    query = '''
        mutation {
            logout {
                success
            }
        }
    '''

    expected = {
        'logout': {
            'success': True,
        },
    }

    result = schema.execute(query, context_value=request_with_session)

    assert not result.errors
    assert result.data == expected


@pytest.mark.django_db
def test_logout_snapshot(schema, snapshot, request_with_session):
    query = '''
        mutation {
            logout {
                success
            }
        }
    '''

    result = schema.execute(query, context_value=request_with_session)

    snapshot.assert_match(result.data)


@pytest.mark.django_db
def test_update_mutation_success(schema, rf, user):
    request = rf.request()
    request.user = user

    query = '''
        mutation Update($first_name: String) {
            update(firstName: $first_name) {
                success
                user {
                    firstName
                }
            }
        }   
    '''

    expected = {
        'update': {
            'success': True,
            'user': {
                'firstName': 'Mark',
            }
        }
    }

    result = schema.execute(query, context_value=request, variable_values={'first_name': 'Mark'})

    assert not result.errors
    assert result.data == expected
