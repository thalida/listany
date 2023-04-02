import graphene
from authentication.schema import AuthQuery, AuthMutation


class Query(AuthQuery, graphene.ObjectType):
    pass


class Mutation(AuthMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
