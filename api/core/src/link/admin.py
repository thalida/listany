from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin

from core.src.link.model import Link


@admin.register(Link)
class LinkAdmin(ModelAdmin):
    actions = ["noop_action"]

    @admin.action(description=_(""))
    def noop_action(self, request, obj):
        pass

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs

        return qs.filter(
            collections__created_by=request.user
        ).distinct()
