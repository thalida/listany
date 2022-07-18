from django.contrib.auth import get_user_model

import graphene
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType
from graphql_auth import relay


class MyUserNode(DjangoObjectType):
    class Meta():
        model = get_user_model()
        filter_fields = ["username"]
        exclude = ["email", "password"]
        interfaces = (graphene.relay.Node, )

    pk = graphene.UUID()


class UserQuery(graphene.ObjectType):
    user = graphene.relay.Node.Field(MyUserNode)
    users = DjangoFilterConnectionField(MyUserNode)


class MeQuery(graphene.ObjectType):
    me = graphene.Field(MyUserNode)

    def resolve_me(self, info):
        user = info.context.user
        if user.is_authenticated:
            return user
        return None


class AuthMutation(graphene.ObjectType):
    token_auth = relay.ObtainJSONWebToken.Field()
    verify_token = relay.VerifyToken.Field()
    refresh_token = relay.RefreshToken.Field()
    revoke_token = relay.RevokeToken.Field()


class Query(UserQuery, MeQuery, graphene.ObjectType):
    pass


class UserMutation(AuthMutation, graphene.ObjectType):
    pass
