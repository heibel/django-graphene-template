import graphene
from jwt import InvalidTokenError

from django.contrib.auth import authenticate, get_user_model
from django.core import signing
from django.db import IntegrityError

from .schema import UserType
from .utils import (
    jwt_decode_handler,
    jwt_encode_handler,
    jwt_payload_handler,
    login_required,
    parse_name,
    password_reset_token_generator,
    send_activation_email,
    send_password_reset_email,
    send_welcome_email,
)


class Register(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)
        name = graphene.String(required=True)

    success = graphene.Boolean()
    errors = graphene.List(graphene.String)

    def mutate(self, info, email, password, name):
        try:
            parsed_name = parse_name(name)
            user = get_user_model().objects.create_user(
                email=email, password=password, **parsed_name
            )

            send_activation_email(user)

            return Register(success=user, errors=None)
        except IntegrityError:
            errors = ["Email already registered."]

            return Register(success=False, errors=errors)


class Activate(graphene.Mutation):
    class Arguments:
        activation_token = graphene.String(required=True)

    success = graphene.Boolean()
    errors = graphene.List(graphene.String)

    def mutate(self, info, activation_token):
        try:
            email = signing.loads(activation_token, max_age=(60 * 12))
            user = get_user_model().objects.get(email=email)
            user.is_active = True
            user.save()

            send_welcome_email(user)

            return Activate(success=True, errors=None)
        except get_user_model().DoesNotExist:
            return Activate(success=False, errors=["Unknown user"])
        except signing.BadSignature:
            return Activate(success=False, errors=["Stale token"])


class Login(graphene.Mutation):
    class Arguments:
        email = graphene.String()
        password = graphene.String()

    success = graphene.Boolean()
    errors = graphene.List(graphene.String)
    token = graphene.String()

    def mutate(self, _, email, password):
        user = authenticate(email=email, password=password)

        if not user:
            return Login(success=False, errors=["Email and/or password are unknown"])

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        return Login(success=True, errors=None, token=token)


class RefreshToken(graphene.Mutation):
    class Arguments:
        token = graphene.String(required=True)

    success = graphene.Boolean()
    errors = graphene.List(graphene.String)
    token = graphene.String()

    def mutate(self, _, token):
        try:
            payload = jwt_decode_handler(token)
        except InvalidTokenError:
            return RefreshToken(success=False, errors=["Invalid token"])

        user = get_user_model().objects.get(email=payload.get("email"))
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        return RefreshToken(success=True, token=token)


class PasswordReset(graphene.Mutation):
    class Arguments:
        email = graphene.String()

    success = graphene.Boolean()

    def mutate(self, info, email):
        try:
            user = get_user_model().objects.get(email=email)
            send_password_reset_email(user)
        except get_user_model().DoesNotExist:
            pass

        return PasswordReset(success=True)


class PasswordResetConfirm(graphene.Mutation):
    class Arguments:
        email = graphene.String()
        password = graphene.String()
        password_repeat = graphene.String()
        password_reset_token = graphene.String()

    success = graphene.Boolean()
    errors = graphene.List(graphene.String)

    def mutate(self, _, email, password, password_repeat, password_reset_token):
        if password != password_repeat:
            return PasswordResetConfirm(success=False, errors=["Passwords don't match"])

        try:
            user = get_user_model().objects.get(email=email)
        except get_user_model().DoesNotExist:
            return PasswordResetConfirm(success=False, errors=["Unknown user"])

        if not password_reset_token_generator.check_token(user, password_reset_token):
            return PasswordResetConfirm(success=False, errors=["Stale token"])

        if not user.is_active or not user.has_usable_password():
            return PasswordResetConfirm(success=False, errors=["Inactive user"])

        user.set_password(password)
        user.save()

        return PasswordResetConfirm(success=True)


class Update(graphene.Mutation):
    class Arguments:
        first_name = graphene.String()
        last_name = graphene.String()

    success = graphene.Boolean()
    errors = graphene.List(graphene.String)
    user = graphene.Field(UserType)

    @login_required
    def mutate(self, info, **fields):
        user = info.context.user

        for attr, value in fields.items():
            setattr(user, attr, value)
        user.save()

        return Update(success=True, errors=None, user=user)


class UserMutation(object):
    register = Register.Field()
    activate = Activate.Field()
    login = Login.Field()
    refresh_token = RefreshToken.Field()
    password_reset = PasswordReset.Field()
    password_reset_confirm = PasswordResetConfirm.Field()
    update = Update.Field()
