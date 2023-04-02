from django.contrib import admin
from django.core.exceptions import ValidationError
from unfold.forms import AuthenticationForm as UnfoldAuthenticationForm


class AuthenticationForm(UnfoldAuthenticationForm):
    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise ValidationError(
                self.error_messages["inactive"],
                code="inactive",
            )


def has_permission(request):
    return request.user.is_active


admin.site.has_permission = has_permission
admin.site.login_form = AuthenticationForm
admin.site.login_template = "unfold_admin/login.html"
