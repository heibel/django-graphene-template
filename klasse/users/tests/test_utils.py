from klasse.users.utils import send_activation_email, send_welcome_email


def test_send_activation_email(user, mailoutbox):
    send_activation_email(user)

    assert len(mailoutbox) == 1


def test_send_welcome_email(user, mailoutbox):
    send_welcome_email(user)

    assert len(mailoutbox) == 1


def send_password_reset_email(user, mailoutbox):
    send_welcome_email(user)

    assert len(mailoutbox) == 1
