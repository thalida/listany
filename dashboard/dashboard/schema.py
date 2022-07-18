import graphene
from users.schema import UserQuery, UserMutation
from links.schema import LinkQuery, LinkMutation


class Query(UserQuery, LinkQuery, graphene.ObjectType):
    pass


class Mutation(UserMutation, LinkMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
