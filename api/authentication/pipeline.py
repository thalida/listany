from django.contrib.auth.models import Group


def assign_default_groups(backend, user, response, *args, **kwargs):
    basic_user_group = Group.objects.get(name='basic_user')
    basic_user_group.user_set.add(user)
