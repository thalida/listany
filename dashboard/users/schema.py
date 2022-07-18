import graphene
from graphql_auth.schema import UserQuery, MeQuery
from graphql_auth import relay


class AuthMutation(graphene.ObjectType):
    token_auth = relay.ObtainJSONWebToken.Field()
    verify_token = relay.VerifyToken.Field()
    refresh_token = relay.RefreshToken.Field()
    revoke_token = relay.RevokeToken.Field()


class Query(UserQuery, MeQuery, graphene.ObjectType):
    pass


class UserMutation(AuthMutation, graphene.ObjectType):
    pass
