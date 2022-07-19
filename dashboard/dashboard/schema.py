import graphene
from users.schema import UserQuery, UserMutation
from bookmarks.schema import BookmarkQuery, BookmarkMutation


class Query(UserQuery, BookmarkQuery, graphene.ObjectType):
    pass


class Mutation(UserMutation, BookmarkMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
