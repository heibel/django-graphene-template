import graphene

from django.contrib.auth import authenticate, get_user_model, login, logout
from django.core import signing
from django.db import IntegrityError

from .schema import UserType
from .utils import parse_name, send_activation_email, send_welcome_email


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
                email=email, password=password, **parsed_name)

            send_activation_email(user, request=info.context)

            return Register(success=user, errors=None)
        except IntegrityError:
            errors = ['Email already registered.']

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

            send_welcome_email(user, request=info.context)

            return Activate(success=True, errors=None)
        except get_user_model().DoesNotExist:
            return Activate(success=False, errors=['Unknown user'])
        except signing.BadSignature:
            return Activate(success=False, errors=['Stale token'])


class Login(graphene.Mutation):

    class Arguments:
        email = graphene.String()
        password = graphene.String()

    success = graphene.Boolean()
    errors = graphene.List(graphene.String)

    def mutate(self, info, email, password):
        user = authenticate(email=email, password=password)

        if user is not None:
            login(info.context, user)

            return Login(success=True, errors=None)

        return Login(success=False, errors=['Email and/or password are unknown'])


class Logout(graphene.Mutation):
    success = graphene.Boolean()

    def mutate(self, info):
        logout(info.context)

        return Logout(success=True)


class Update(graphene.Mutation):

    class Arguments:
        first_name = graphene.String()
        last_name = graphene.String()

    success = graphene.Boolean()
    errors = graphene.List(graphene.String)
    user = graphene.Field(UserType)

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
    logout = Logout.Field()
    update = Update.Field()
