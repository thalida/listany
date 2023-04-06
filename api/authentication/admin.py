from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin, GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from social_django.admin import UserSocialAuthOption as BaseUserSocialAuthAdmin
from social_django.models import UserSocialAuth
from unfold.admin import ModelAdmin
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm
from unfold.decorators import display

from authentication.models import User


admin.site.unregister(Group)
admin.site.unregister(UserSocialAuth)


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm

    list_display = ("username", "email", "first_name",
                    "last_name", "is_staff", "show_groups")

    @display(description=_("Groups"), ordering="groups")
    def show_groups(self, obj):
        return ", ".join([group.name for group in obj.groups.all()])


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass


@admin.register(UserSocialAuth)
class UserSocialAuthAdmin(BaseUserSocialAuthAdmin, ModelAdmin):
    pass
