from django.contrib import admin
from django.db.models import Q
from django.forms.widgets import TextInput
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin
from unfold.decorators import display

from authentication.models import User
from core.src.user_tag.model import UserTag


@admin.register(UserTag)
class UserTagAdmin(ModelAdmin):
    list_display = ("tag_with_color", "description", "show_collections")
    actions = ["noop_action"]

    @admin.action(description=_(""))
    def noop_action(self, request, obj):
        pass

    @display(description=_("Tag"), label=True)
    def tag_with_color(self, obj):
        return format_html(
            "<span style='color: {color}'>{tag}</span>",
            color=obj.color,
            tag=obj.tag.label,
        )

    @display(description=_("Collections"))
    def show_collections(self, obj):
        collections = [
            {
                "url": reverse("admin:core_collection_change", args=[collection.pk]),
                "title": collection.title,
            }
            for collection in obj.collections.all()
        ]
        html_arr = [
            "<a href='{url}'>{title}</a>".format(
                url=collection["url"], title=collection["title"]
            )
            for collection in collections
        ]
        return format_html(", ".join(html_arr))

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs

        return qs.filter(Q(user=request.user.pk)).distinct()

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.is_superuser:
            form.base_fields["user"].queryset = User.objects.filter(pk=request.user.pk)

        form.base_fields["color"].widget = TextInput(attrs={"type": "color"})
        return form

    def get_changeform_initial_data(self, request):
        return {
            "user": request.user.pk,
        }
