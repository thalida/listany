import graphene

from authentication.schema import AuthMutation, AuthQuery
from core.schema import CoreMutation, CoreQuery


class Query(AuthQuery, CoreQuery, graphene.ObjectType):
    pass


class Mutation(AuthMutation, CoreMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
