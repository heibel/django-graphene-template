from unittest import mock

import pytest

from django.core import signing

from klasse.users.utils import (
    generate_activation_token,
    jwt_encode_handler,
    jwt_payload_handler,
    password_reset_token_generator,
)


@pytest.mark.django_db
def test_register_mutation_success(schema, mailoutbox):
    query = """
        mutation Register($email: String!, $password: String!, $name: String!) {
            register(email: $email, password: $password, name: $name) {
                success
                errors
            }
        }
    """

    variables = {
        "email": "user@example.com",
        "password": "password",
        "name": "John Doe",
    }

    expected = {"register": {"success": True, "errors": None}}

    result = schema.execute(query, variable_values=variables)

    assert not result.errors
    assert result.data == expected
    assert len(mailoutbox) == 1


@pytest.mark.django_db
def test_register_mutation_error(schema):
    query = """
        mutation Register($email: String!, $password: String!, $name: String!) {
            register(email: $email, password: $password, name: $name) {
                success
                errors
            }
        }
    """

    variables = {
        "email": "user@example.com",
        "password": "password",
        "name": "John Doe",
    }

    expected = {"register": {"success": False, "errors": ["Email already registered."]}}

    schema.execute(query, variable_values=variables)

    result = schema.execute(query, variable_values=variables)

    assert not result.errors
    assert result.data == expected


@pytest.mark.django_db
def test_register_snapshot(schema, snapshot, mailoutbox):
    query = """
        mutation Register($email: String!, $password: String!, $name: String!) {
            register(email: $email, password: $password, name: $name) {
                success
                errors
            }
        }
    """

    variables = {
        "email": "user@example.com",
        "password": "password",
        "name": "John Doe",
    }

    result = schema.execute(query, variable_values=variables)

    snapshot.assert_match(result.data)
    snapshot.assert_match(mailoutbox[0].subject)


def test_activate_mutation_success(schema, user, mailoutbox):
    activation_token = generate_activation_token(user)

    query = """
        mutation Activate($activation_token: String!) {
            activate(activationToken: $activation_token) {
                success
                errors
            }
        }
    """

    variables = {"activation_token": activation_token}

    expected = {"activate": {"success": True, "errors": None}}

    result = schema.execute(query, variable_values=variables)

    user.refresh_from_db()

    assert not result.errors
    assert result.data == expected

    assert user.is_active
    assert len(mailoutbox) == 1


def test_activate_mutation_user_error(schema, user):
    activation_token = generate_activation_token(user)

    query = """
        mutation Activate($activation_token: String!) {
            activate(activationToken: $activation_token) {
                success
                errors
            }
        }
    """

    variables = {"activation_token": activation_token}

    expected = {"activate": {"success": False, "errors": ["Unknown user"]}}

    with mock.patch(
        "klasse.users.mutations.signing.loads", return_value="unknown@example.com"
    ):
        result = schema.execute(query, variable_values=variables)

    assert not result.errors
    assert result.data == expected


def test_activate_mutation_token_error(schema, user):
    activation_token = generate_activation_token(user)

    query = """
        mutation Activate($activation_token: String!) {
            activate(activationToken: $activation_token) {
                success
                errors
            }
        }
    """

    variables = {"activation_token": activation_token}

    expected = {"activate": {"success": False, "errors": ["Stale token"]}}

    with mock.patch(
        "klasse.users.mutations.signing.loads", side_effect=signing.BadSignature
    ):
        result = schema.execute(query, variable_values=variables)

    assert not result.errors
    assert result.data == expected


def test_activate_mutation_snapshot(schema, user, mailoutbox, snapshot):
    activation_token = generate_activation_token(user)

    query = """
        mutation Activate($activation_token: String!) {
            activate(activationToken: $activation_token) {
                success
                errors
            }
        }
    """

    variables = {"activation_token": activation_token}

    result = schema.execute(query, variable_values=variables)

    snapshot.assert_match(result.data)
    snapshot.assert_match(mailoutbox[0].subject)


def test_login_mutation_success(schema, user):
    user.is_active = True
    user.save()

    query = """
        mutation Login($email: String!, $password: String!) {
            login(email: $email, password: $password) {
                success
                errors
                token
            }
        }
    """

    variables = {"email": "user@example.com", "password": "password"}

    expected = {"login": {"success": True, "errors": None, "token": "sample.jwt.token"}}

    with mock.patch("klasse.users.utils.jwt.encode", return_value=b"sample.jwt.token"):
        result = schema.execute(query, variable_values=variables)

    assert not result.errors
    assert result.data == expected


@pytest.mark.django_db
def test_login_mutation_error(schema):
    query = """
        mutation Login($email: String!, $password: String!) {
            login(email: $email, password: $password) {
                success
                errors
                token
            }
        }
    """

    variables = {"email": "user@example.com", "password": "password"}

    expected = {
        "login": {
            "success": False,
            "errors": ["Email and/or password are unknown"],
            "token": None,
        }
    }

    result = schema.execute(query, variable_values=variables)

    assert not result.errors
    assert result.data == expected


def test_login_snapshot(schema, user, snapshot):
    user.is_active = True
    user.save()

    query = """
        mutation Login($email: String!, $password: String!) {
            login(email: $email, password: $password) {
                success
                errors
                token
            }
        }
    """

    variables = {
        "email": "user@example.com",
        "password": "password",
        "token": "sample.jwt.token",
    }

    with mock.patch("klasse.users.utils.jwt.encode", return_value=b"sample.jwt.token"):
        result = schema.execute(query, variable_values=variables)

    snapshot.assert_match(result.data)


def test_refresh_token_success(schema, user):
    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)

    query = """
        mutation RefreshToken($token: String!) {
            refreshToken(token: $token) {
                success
                token
            }
        }
    """

    variables = {"token": token}

    expected = {"refreshToken": {"success": True, "token": "sample.jwt.token"}}

    with mock.patch("klasse.users.utils.jwt.encode", return_value=b"sample.jwt.token"):
        result = schema.execute(query, variable_values=variables)

    assert not result.errors
    assert result.data == expected


def test_refresh_token_error(schema):
    query = """
        mutation RefreshToken($token: String!) {
            refreshToken(token: $token) {
                success
                errors
            }
        }
    """

    variables = {"token": "invalid.jwt.token"}

    expected = {"refreshToken": {"success": False, "errors": ["Invalid token"]}}

    result = schema.execute(query, variable_values=variables)

    assert not result.errors
    assert result.data == expected


def test_password_reset_mutation_success(schema, user, mailoutbox):
    user.is_active = True
    user.save()

    query = """
        mutation PasswordReset($email: String!) {
            passwordReset(email: $email) {
                success
            }
        }
    """

    variables = {"email": "user@example.com"}

    expected = {"passwordReset": {"success": True}}

    result = schema.execute(query, variable_values=variables)

    assert not result.errors
    assert result.data == expected
    assert len(mailoutbox) == 1


@pytest.mark.django_db
def test_password_reset_mutation_error(schema, mailoutbox):
    query = """
        mutation PasswordReset($email: String!) {
            passwordReset(email: $email) {
                success
            }
        }
    """

    variables = {"email": "unknown@example.com"}

    expected = {"passwordReset": {"success": True}}

    result = schema.execute(query, variable_values=variables)

    assert not result.errors
    assert result.data == expected
    assert len(mailoutbox) == 0


def test_password_reset_confirm_mutation_success(schema, user):
    user.is_active = True
    user.save()

    query = """
        mutation PasswordResetConfirm(
            $email: String!,
            $password: String!,
            $password_repeat: String!,
            $password_reset_token: String!
        ) {
            passwordResetConfirm(
                email: $email,
                password: $password,
                passwordRepeat: $password_repeat,
                passwordResetToken: $password_reset_token
            ) {
                success
                errors
            }
        }
    """

    variables = {
        "email": "user@example.com",
        "password": "p@ssword!",
        "password_repeat": "p@ssword!",
        "password_reset_token": password_reset_token_generator.make_token(user),
    }

    expected = {"passwordResetConfirm": {"success": True, "errors": None}}

    result = schema.execute(query, variable_values=variables)

    assert not result.errors
    assert result.data == expected


def test_password_reset_confirm_mutation_matching_passwords_error(schema, user):
    user.is_active = True
    user.save()

    query = """
        mutation PasswordResetConfirm(
            $email: String!,
            $password: String!,
            $password_repeat: String!,
            $password_reset_token: String!
        ) {
            passwordResetConfirm(
                email: $email,
                password: $password,
                passwordRepeat: $password_repeat,
                passwordResetToken: $password_reset_token
            ) {
                success
                errors
            }
        }
    """

    variables = {
        "email": "user@example.com",
        "password": "p@ssword!",
        "password_repeat": "p@ssw0rd!",
        "password_reset_token": password_reset_token_generator.make_token(user),
    }

    expected = {
        "passwordResetConfirm": {"success": False, "errors": ["Passwords don't match"]}
    }

    result = schema.execute(query, variable_values=variables)

    assert not result.errors
    assert result.data == expected


def test_password_reset_confirm_mutation_unknown_user_error(schema, user):
    user.is_active = True
    user.save()

    query = """
        mutation PasswordResetConfirm(
            $email: String!,
            $password: String!,
            $password_repeat: String!,
            $password_reset_token: String!
        ) {
            passwordResetConfirm(
                email: $email,
                password: $password,
                passwordRepeat: $password_repeat,
                passwordResetToken: $password_reset_token
            ) {
                success
                errors
            }
        }
    """

    variables = {
        "email": "unknown@example.com",
        "password": "p@ssword!",
        "password_repeat": "p@ssword!",
        "password_reset_token": password_reset_token_generator.make_token(user),
    }

    expected = {"passwordResetConfirm": {"success": False, "errors": ["Unknown user"]}}

    result = schema.execute(query, variable_values=variables)

    assert not result.errors
    assert result.data == expected


def test_password_reset_confirm_mutation_token_error(schema, user):
    user.is_active = True
    user.save()

    query = """
        mutation PasswordResetConfirm(
            $email: String!,
            $password: String!,
            $password_repeat: String!,
            $password_reset_token: String!
        ) {
            passwordResetConfirm(
                email: $email,
                password: $password,
                passwordRepeat: $password_repeat,
                passwordResetToken: $password_reset_token
            ) {
                success
                errors
            }
        }
    """

    variables = {
        "email": "user@example.com",
        "password": "p@ssword!",
        "password_repeat": "p@ssword!",
        "password_reset_token": "12345",
    }

    expected = {"passwordResetConfirm": {"success": False, "errors": ["Stale token"]}}

    result = schema.execute(query, variable_values=variables)

    assert not result.errors
    assert result.data == expected


def test_password_reset_confirm_mutation_inactive_user_error(schema, user):
    query = """
        mutation PasswordResetConfirm(
            $email: String!,
            $password: String!,
            $password_repeat: String!,
            $password_reset_token: String!
        ) {
            passwordResetConfirm(
                email: $email,
                password: $password,
                passwordRepeat: $password_repeat,
                passwordResetToken: $password_reset_token
            ) {
                success
                errors
            }
        }
    """

    variables = {
        "email": "user@example.com",
        "password": "p@ssword!",
        "password_repeat": "p@ssword!",
        "password_reset_token": password_reset_token_generator.make_token(user),
    }

    expected = {"passwordResetConfirm": {"success": False, "errors": ["Inactive user"]}}

    result = schema.execute(query, variable_values=variables)

    assert not result.errors
    assert result.data == expected


def test_update_mutation_success(schema, rf, user):
    request = rf.request()
    request.user = user

    query = """
        mutation Update($first_name: String) {
            update(firstName: $first_name) {
                success
                user {
                    firstName
                }
            }
        }
    """

    expected = {"update": {"success": True, "user": {"firstName": "Mark"}}}

    result = schema.execute(
        query, context_value=request, variable_values={"first_name": "Mark"}
    )

    assert not result.errors
    assert result.data == expected
