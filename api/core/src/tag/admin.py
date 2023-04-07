from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin

from authentication.models import User
from core.src.tag.model import Tag


@admin.register(Tag)
class TagAdmin(ModelAdmin):
    actions = ["noop_action"]

    @admin.action(description=_(""))
    def noop_action(self, request, obj):
        pass

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.is_superuser:
            form.base_fields["created_by"].queryset = User.objects.filter(
                pk=request.user.pk
            )
        return form

    def get_changeform_initial_data(self, request):
        return {
            "created_by": request.user.pk,
        }
