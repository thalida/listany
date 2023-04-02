import functools


def login_required(func):

    @functools.wraps(func)
    def wrapper(self, root, info, **kwargs):
        if info.context.user.is_anonymous:
            raise Exception('403: Unauthorized')
        res = func(self, root, info, **kwargs)
        return res

    return wrapper


class IsAuthenticated:
    @classmethod
    @login_required
    def get_queryset(cls, queryset, info):
        return queryset
