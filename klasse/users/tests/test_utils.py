import mock

from klasse.users.utils import (
    send_activation_email,
    send_password_reset_email,
    send_welcome_email,
)


def test_send_activation_email(user, mailoutbox, snapshot):
    with mock.patch(
        "klasse.users.utils.generate_activation_token", return_value="secret"
    ):
        send_activation_email(user)

    snapshot.assert_match(mailoutbox[0].body)


def test_send_welcome_email(user, mailoutbox, snapshot):
    send_welcome_email(user)

    snapshot.assert_match(mailoutbox[0].body)


def test_send_password_reset_email(user, mailoutbox, snapshot):
    with mock.patch(
        "klasse.users.utils.generate_password_reset_token", return_value="secret"
    ):
        send_password_reset_email(user)

    snapshot.assert_match(mailoutbox[0].body)
