from nameparser import HumanName

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core import signing

from klasse.users.emails import ActivationEmail, PasswordResetEmail, WelcomeEmail

password_reset_token_generator = PasswordResetTokenGenerator()


def generate_activation_token(user):
    return signing.dumps(obj=user.email)


def generate_password_reset_token(user):
    return password_reset_token_generator.make_token(user=user)


def parse_name(name):
    human_name = HumanName(name)

    return dict(
        first_name=human_name.first,
        middle_name=human_name.middle,
        last_name=human_name.last,
    )


def send_activation_email(user, request=None):
    activation_email = ActivationEmail(
        request=request,
        context={
            'user': user,
            'activation_token': generate_activation_token(user)
        })

    activation_email.send(to=[user.email])


def send_welcome_email(user, request=None):
    welcome_email = WelcomeEmail(
        request=request, context={
            'user': user,
        })

    welcome_email.send(to=[user.email])


def send_password_reset_email(user, request=None):
    password_reset_email = PasswordResetEmail(
        request=request,
        context={
            'user': user,
            'password_reset_token': generate_password_reset_token(user)
        })

    password_reset_email.send(to=[user.email])
