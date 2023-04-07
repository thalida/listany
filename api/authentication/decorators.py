from functools import wraps

import graphql_jwt.signals
from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import gettext as _
from graphene.utils.thenables import maybe_thenable
from graphql_jwt.decorators import (
    csrf_rotation,
    on_token_auth_resolve,
    refresh_expiration,
    setup_jwt_cookie,
)
from graphql_jwt.exceptions import JSONWebTokenError


def token_auth_email(f):
    @wraps(f)
    @setup_jwt_cookie
    @csrf_rotation
    @refresh_expiration
    def wrapper(cls, root, info, password, **kwargs):
        context = info.context
        context._jwt_token_auth = True
        email = kwargs.get(get_user_model().EMAIL_FIELD)

        user = authenticate(
            request=context,
            username=email,
            password=password,
        )
        print(user)
        if user is None:
            raise JSONWebTokenError(
                _("Please enter valid credentials"),
            )

        if hasattr(context, "user"):
            context.user = user

        result = f(cls, root, info, **kwargs)
        graphql_jwt.signals.token_issued.send(sender=cls, request=context, user=user)
        return maybe_thenable((context, user, result), on_token_auth_resolve)

    return wrapper
