import typing
import strawberry

from authentication.schema import Query as AuthenticationQuery, Mutation as AuthenticationMutation


@strawberry.type
class Query(AuthenticationQuery):
    pass


@strawberry.type
class Mutation(AuthenticationMutation):
    pass


schema = strawberry.Schema(query=Query, mutation=Mutation)
