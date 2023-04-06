import graphene
from authentication.schema import AuthQuery, AuthMutation
from core.schema import CoreQuery, CoreMutation


class Query(AuthQuery, CoreQuery, graphene.ObjectType):
    pass


class Mutation(AuthMutation, CoreMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
