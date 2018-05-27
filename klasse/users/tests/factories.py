import factory
from factory.django import DjangoModelFactory

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group


class UserFactory(DjangoModelFactory):

    class Meta:
        model = get_user_model()
        django_get_or_create = ("email",)

    email = factory.Faker("email")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")


class GroupFactory(DjangoModelFactory):

    class Meta:
        model = Group
        django_get_or_create = ("name",)

    name = factory.Sequence(lambda n: "group.{}".format(n + 1))
