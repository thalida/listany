from django.contrib import admin
from django.db import models
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin
from unfold.contrib.forms.widgets import WysiwygWidget
from unfold.decorators import display

from authentication.models import User
from core.src.collection.model import Collection
from core.src.collection_link.model import CollectionLink


@admin.register(CollectionLink)
class CollectionLinkAdmin(ModelAdmin):
    list_display = (
        "show_link_with_url",
        "formatted_note",
        "collection",
        "updated_at",
        "open_link",
    )
    list_filter = (
        "link__url",
        "collection",
        "updated_at",
        "created_at",
    )
    actions = ["noop_action"]
    list_select_related = True
    list_filter_submit = True

    formfield_overrides = {
        models.TextField: {"widget": WysiwygWidget},
    }

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs

        return qs.filter(collection__created_by=request.user).distinct()

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.is_superuser:
            form.base_fields["created_by"].queryset = User.objects.filter(
                pk=request.user.pk
            )
            form.base_fields["collection"].queryset = Collection.objects.filter(
                created_by=request.user.pk
            )
        return form

    def get_changeform_initial_data(self, request):
        return {
            "created_by": request.user.pk,
        }

    @display(header=True, description=_("Link"), ordering="link")
    def show_link_with_url(self, obj):
        return obj.link.title, obj.link.url

    @display(description=_("Note"))
    def formatted_note(self, obj):
        return format_html(obj.note)

    @display(description=_(""))
    def open_link(self, obj):
        return format_html(
            "<a href='{url}' target='_blank'><span class='material-symbols-outlined md-18 mr-3'>open_in_new</span></a>",
            url=obj.link.url,
        )

    @admin.action(description=_(""))
    def noop_action(self, request, obj):
        pass
