import factory
from factory.django import DjangoModelFactory

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group


class UserFactory(DjangoModelFactory):
    email = factory.Sequence(lambda n: 'user.{}@example.com'.format(n + 1))

    class Meta:
        model = get_user_model()
        django_get_or_create = ('email', )


class GroupFactory(DjangoModelFactory):
    name = factory.Sequence(lambda n: 'group.{}'.format(n + 1))

    class Meta:
        model = Group
        django_get_or_create = ('name', )
