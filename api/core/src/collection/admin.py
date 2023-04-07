from django.contrib import admin
from django.db import models
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin
from unfold.contrib.forms.widgets import WysiwygWidget
from unfold.decorators import display

from authentication.models import User
from core.src.collection.model import Collection
from core.src.user_tag.model import UserTag


@admin.register(Collection)
class CollectionAdmin(ModelAdmin):
    list_display = (
        "show_title_and_subtitle",
        "show_tags",
        "is_public",
        "updated_at",
        "show_links_link",
    )

    list_filter = (
        "is_public",
        "tags__tag",
    )

    actions = ["noop_action"]

    formfield_overrides = {
        models.TextField: {"widget": WysiwygWidget},
    }

    @admin.action(description=_(""))
    def noop_action(self, request, obj):
        pass

    @display(header=True, description=_("Collection"), ordering="title")
    def show_title_and_subtitle(self, obj):
        return obj.title, obj.subtitle

    @display(description=_(""), ordering="links")
    def show_links_link(self, obj):
        return format_html(
            f"<a href='{reverse('admin:core_collectionlink_changelist')}?"
            f"collection__uid__exact={obj.uid}' class='flex justify-items-center space-x-2'>"
            f"<span>View {obj.links.count()} link(s)</span>"
            "<span class='material-symbols-outlined md-18'>arrow_forward</span>"
            "</a>"
        )

    @display(description=_("Tags"), ordering="tags")
    def show_tags(self, obj):
        tags_html = [
            (
                f"<a href='{reverse('admin:core_usertag_change', args=[tag.pk])}'"
                "class='border border-gray-200 font-semibold leading-none mr-2 px-2 py-1"
                "rounded shadow-sm text-xxs uppercase whitespace-nowrap last:mr-0 bg-white"
                "text-gray-400 dark:bg-white/[.04] dark:border-gray-800 dark:text-gray-400'>"
                f"<span style='color: {tag.color}'>"
                f"{tag.tag.label}"
                "</span>"
                "</a>"
            )
            for tag in obj.tags.all()
        ]
        return format_html("".join(tags_html))

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(created_by=request.user)

    def get_form(self, request, obj=None, **kwargs):
        form = super(CollectionAdmin, self).get_form(request, obj, **kwargs)
        if not request.user.is_superuser:
            form.base_fields["created_by"].queryset = User.objects.filter(
                pk=request.user.pk
            )
            form.base_fields["tags"].queryset = UserTag.objects.filter(
                user=request.user
            )
        return form

    def get_changeform_initial_data(self, request):
        return {
            "created_by": request.user.pk,
        }
