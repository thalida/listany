from django.db import models
from django.db.models import Q
from django.contrib import admin
from django.urls import reverse, reverse_lazy
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from authentication.models import User
from core.models import Link, Collection, CollectionLink, Tag, UserTag
from unfold.admin import ModelAdmin, TabularInline, StackedInline
from unfold.contrib.forms.widgets import WysiwygWidget
from unfold.decorators import action, display


@admin.register(Collection)
class CollectionAdmin(ModelAdmin):
    list_display = (
        "show_title_and_subtitle",
        "show_num_links",
        "show_tags",
        "is_public",
        "updated_at",
    )

    formfield_overrides = {
        models.TextField: {'widget': WysiwygWidget},
    }

    @display(header=True, description=_("Collection"), ordering="title")
    def show_title_and_subtitle(self, obj):
        return obj.title, obj.subtitle

    @display(description=_("Total Links"), ordering="links")
    def show_num_links(self, obj):
        return obj.links.count()

    @display(description=_("Tags"), ordering="tags")
    def show_tags(self, obj):
        return ", ".join([tag.tag.label for tag in obj.tags.all()])

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
        "link",
        "collection",
        "formatted_note",
        "updated_at",
        "open_link",
    )
    list_filter = (
        "link__url",
        "collection__title",
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
        "tag",
        "color",
        "description",
        "show_collections"
    )

    @display(description=_("Collections"))
    def show_collections(self, obj):
        return ", ".join([collection.title for collection in obj.collections.all()])

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
        return form

    def get_changeform_initial_data(self, request):
        return {
            'user': request.user.pk,
        }
