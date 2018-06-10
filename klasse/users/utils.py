import datetime
from calendar import timegm
from functools import wraps

import jwt
from nameparser import HumanName

from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core import signing
from django.core.exceptions import PermissionDenied

from klasse.users.emails import ActivationEmail, PasswordResetEmail, WelcomeEmail

password_reset_token_generator = PasswordResetTokenGenerator()

secret_key = settings.SECRET_KEY


def login_required(func):
    @wraps(func)
    def decorator(cls, info, *args, **kwargs):
        if not info.context.user.is_authenticated:
            raise PermissionDenied("Not allowed")

        return func(cls, info, *args, **kwargs)

    return decorator


def jwt_encode_handler(payload):
    return jwt.encode(payload, secret_key, algorithm="HS256").decode("utf-8")


def jwt_decode_handler(token):
    return jwt.decode(token, secret_key, algorithm="HS256")


def jwt_payload_handler(user):
    return {
        "email": user.email,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
        "orig_iat": timegm(datetime.datetime.utcnow().utctimetuple()),
    }


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


def send_activation_email(user):
    activation_email = ActivationEmail(
        context={"user": user, "activation_token": generate_activation_token(user)}
    )

    activation_email.send(to=[user.email])


def send_welcome_email(user):
    welcome_email = WelcomeEmail(context={"user": user})

    welcome_email.send(to=[user.email])


def send_password_reset_email(user):
    password_reset_email = PasswordResetEmail(
        context={
            "user": user,
            "password_reset_token": generate_password_reset_token(user),
        }
    )

    password_reset_email.send(to=[user.email])
