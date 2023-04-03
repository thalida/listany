from django.db import IntegrityError
import graphene
from graphene_django.types import DjangoObjectType
import graphql_jwt
from graphql_jwt.decorators import login_required
from graphql_jwt.mixins import ObtainJSONWebTokenMixin
from graph_auth.models import UserStatus
from graph_auth.constants import Messages
from graph_auth.exceptions import EmailAlreadyInUse
from graph_auth.signals import user_registered
from graph_auth.schema import Register, VerifyAccount, ResendActivationEmail, SendPasswordResetEmail, PasswordReset
from social_django.utils import load_strategy, load_backend
from social_django.views import _do_login


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


class RegisterBySocial(graphene.relay.ClientIDMutation):
    class Input:
        access_token = graphene.String(required=True)
        social_backend = graphene.String(required=True)

    user = graphene.Field(UserNode)
    token = graphene.String()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        social_strategy = load_strategy()
        social_backend = load_backend(
            social_strategy,
            input['social_backend'],
            redirect_uri=None
        )
        user = social_backend.do_auth(input['access_token'])
        _do_login(social_backend, user, user.social_user)
        payload = graphql_jwt.utils.jwt_payload(user)
        token = graphql_jwt.utils.jwt_encode(payload)

        return RegisterBySocial(user=user, token=token)


class RegisterByEmail(Register):
    user = graphene.Field(UserNode)
    token = graphene.String()

    @classmethod
    def login_on_register(cls, root, info, user, **kwargs):
        info.context.POST = {
            'email': user.email,
            'password': user.password
        }
        strategy = load_strategy(info.context)
        backend = load_backend(
            strategy,
            'email',
            redirect_uri=None
        )
        _do_login(backend, user, user)

        payload = graphql_jwt.utils.jwt_payload(user)
        token = graphql_jwt.utils.jwt_encode(payload)

        return token

    @classmethod
    def perform_mutation(cls, root, info, **kwargs):
        """
        register(
            email: String!
            username: String!
            password: String!
        ): Register
        """
        try:
            email = kwargs.get("email")
            password = kwargs.get("password")
            username = kwargs.get("username")
            # clean email
            UserStatus.clean_email(email)
            # create user
            user = User.objects.create_user(
                email=email, password=password, username=username
            )

            user_registered.send(sender=cls, user=user)
            token = cls.login_on_register(root, info, user, **kwargs)

            return cls(
                success=True,
                errors=None,
                user=user,
                token=token
            )
        except IntegrityError:
            return cls(
                success=False,
                errors=[Messages.USERNAME_IN_USE],
                user=None,
                token=None,
            )
        except EmailAlreadyInUse:
            return cls(
                success=False,
                errors=[Messages.EMAIL_IN_USE],
                user=None,
                token=None,
            )
        except Exception as e:
            return cls(
                success=False,
                errors=[Messages.SERVER_ERROR],
                user=None,
                token=None,
            )


class TokenAuth(ObtainJSONWebTokenMixin, graphene.ClientIDMutation):
    class Input:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    user = graphene.Field(UserNode)

    @classmethod
    @token_auth_email
    def mutate_and_get_payload(cls, root, info, **kwargs):
        return cls.resolve(root, info, **kwargs)

    @classmethod
    def resolve(cls, root, info, **kwargs):
        user = info.context.user
        strategy = load_strategy(info.context)
        backend = load_backend(
            strategy,
            'email',
            redirect_uri=None
        )
        _do_login(backend, user, user)
        return cls()


class AuthQuery(graphene.ObjectType):
    user = graphene.relay.Node.Field(UserNode)
    me = graphene.Field(UserNode)

    @login_required
    def resolve_me(self, info):
        return info.context.user


class AuthMutation(graphene.ObjectType):
    token_auth = TokenAuth.Field()
    verify_token = graphql_jwt.relay.Verify.Field()
    refresh_token = graphql_jwt.relay.Refresh.Field()
    revoke_token = graphql_jwt.relay.Revoke.Field()
    delete_token_cookie = graphql_jwt.DeleteJSONWebTokenCookie.Field()
    delete_refresh_token_cookie = graphql_jwt.DeleteRefreshTokenCookie.Field()

    register_social = RegisterBySocial.Field()
    register_email = RegisterByEmail.Field()

    verify_account = VerifyAccount.Field()
    resend_activation_email = ResendActivationEmail.Field()
    send_password_reset_email = SendPasswordResetEmail.Field()
    password_reset = PasswordReset.Field()
