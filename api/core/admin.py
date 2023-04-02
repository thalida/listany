from django.db import models
from django.db.models import Q
from django.contrib import admin
from django.forms.widgets import TextInput
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from authentication.models import User
from core.models import Link, Collection, CollectionLink, Tag, UserTag
from unfold.admin import ModelAdmin
from unfold.contrib.forms.widgets import WysiwygWidget
from unfold.decorators import display


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
        models.TextField: {'widget': WysiwygWidget},
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
            f"<a href='{reverse('admin:core_collectionlink_changelist')}?collection__uid__exact={obj.uid}' class='flex justify-items-center space-x-2'>"
            f"<span>View {obj.links.count()} link(s)</span>"
            f"<span class='material-symbols-outlined md-18'>arrow_forward</span>"
            f"</a>"
        )

    @display(description=_("Tags"), ordering="tags")
    def show_tags(self, obj):
        tags_html = [
            (
                f"<a href='{reverse('admin:core_usertag_change', args=[tag.pk])}' class='border border-gray-200 font-semibold leading-none mr-2 px-2 py-1 rounded shadow-sm text-xxs uppercase whitespace-nowrap last:mr-0 bg-white text-gray-400 dark:bg-white/[.04] dark:border-gray-800 dark:text-gray-400'>"
                f"<span style='color: {tag.color}'>"
                f"{tag.tag.label}"
                f"</span>"
                f"</a>"
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
            form.base_fields['created_by'].queryset = (
                User.objects.filter(pk=request.user.pk)
            )
            form.base_fields['tags'].queryset = (
                UserTag.objects.filter(user=request.user)
            )
        return form

    def get_changeform_initial_data(self, request):
        return {
            'created_by': request.user.pk,
        }


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
        models.TextField: {'widget': WysiwygWidget},
    }

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs

        return qs.filter(
            collection__created_by=request.user
        ).distinct()

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.is_superuser:
            form.base_fields['created_by'].queryset = (
                User.objects.filter(pk=request.user.pk)
            )
            form.base_fields['collection'].queryset = (
                Collection.objects.filter(created_by=request.user.pk)
            )
        return form

    def get_changeform_initial_data(self, request):
        return {
            'created_by': request.user.pk,
        }

    @display(header=True, description=_("Link"), ordering="link")
    def show_link_with_url(self, obj):
        return obj.link.title, obj.link.url

    @display(description=_("Note"))
    def formatted_note(self, obj):
        return format_html(obj.note)

    @display(description=_(""))
    def open_link(self, obj):
        return format_html("<a href='{url}' target='_blank'><span class='material-symbols-outlined md-18 mr-3'>open_in_new</span></a>", url=obj.link.url)

    @admin.action(description=_(""))
    def noop_action(self, request, obj):
        pass


@admin.register(Tag)
class TagAdmin(ModelAdmin):
    actions = ["noop_action"]

    @admin.action(description=_(""))
    def noop_action(self, request, obj):
        pass

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.is_superuser:
            form.base_fields['created_by'].queryset = (
                User.objects.filter(pk=request.user.pk)
            )
        return form

    def get_changeform_initial_data(self, request):
        return {
            'created_by': request.user.pk,
        }


@admin.register(UserTag)
class UserTagAdmin(ModelAdmin):
    list_display = (
        "tag_with_color",
        "description",
        "show_collections"
    )
    actions = ["noop_action"]

    @admin.action(description=_(""))
    def noop_action(self, request, obj):
        pass

    @display(description=_("Tag"), label=True)
    def tag_with_color(self, obj):
        return format_html("<span style='color: {color}'>{tag}</span>", color=obj.color, tag=obj.tag.label)

    @display(description=_("Collections"))
    def show_collections(self, obj):
        collections = [
            {
                "url": reverse("admin:core_collection_change", args=[collection.pk]),
                "title": collection.title
            } for collection in obj.collections.all()
        ]
        html_arr = [
            "<a href='{url}'>{title}</a>".format(url=collection["url"], title=collection["title"]) for collection in collections
        ]
        return format_html(", ".join(html_arr))

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs

        return qs.filter(
            Q(user=request.user.pk)
        ).distinct()

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.is_superuser:
            form.base_fields['user'].queryset = (
                User.objects.filter(pk=request.user.pk)
            )

        form.base_fields['color'].widget = TextInput(attrs={'type': 'color'})
        return form

    def get_changeform_initial_data(self, request):
        return {
            'user': request.user.pk,
        }
