from graphene_django.types import DjangoObjectType

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group


class GroupType(DjangoObjectType):

    class Meta:
        model = Group
        filter_fields = ('name', )


class UserType(DjangoObjectType):

    class Meta:
        model = get_user_model()
