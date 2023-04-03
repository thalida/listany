from django.db import IntegrityError
import graphene
from graphene_django.types import DjangoObjectType


from api.permissions import IsAuthenticated
from authentication.models import User
from authentication.decorators import token_auth_email


class UserNode(IsAuthenticated, DjangoObjectType):
    class Meta():
        model = User
        interfaces = (graphene.relay.Node, )
        filter_fields = [
            "uid",
            "email",
            "username",
            "is_active",
            "is_staff",
            "is_superuser"
        ]
        exclude = ["password"]


class AuthQuery(graphene.ObjectType):
    pass


class AuthMutation(graphene.ObjectType):
    pass
