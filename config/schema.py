import graphene
from graphene_django.debug import DjangoDebug

from klasse.users.mutations import UserMutation
from klasse.users.schema import UserType


class Query(graphene.ObjectType):
    viewer = graphene.Field(UserType)
    debug = graphene.Field(DjangoDebug, name="__debug")

    @staticmethod
    def resolve_viewer(cls, info):
        if info.context.user.is_authenticated:
            return info.context.user

        return None


class Mutation(UserMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
