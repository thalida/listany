import graphene
from django.db import models
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from core.src.tag.model import Tag


class TagNode(DjangoObjectType):
    class Meta:
        model = Tag
        interfaces = (graphene.relay.Node,)
        fields = [
            "uid",
            "created_at",
            "updated_at",
            "slug",
            "label",
            "is_hidden",
        ]
        filter_fields = [
            "uid",
            "created_at",
            "updated_at",
            "slug",
            "label",
            "is_hidden",
        ]

    def get_queryset(self, queryset, info):
        isnt_deleted = models.Q(is_deleted=False)

        return queryset.filter(isnt_deleted)


class CreateTag(graphene.relay.ClientIDMutation):
    class Input:
        slug = graphene.String(required=True)
        label = graphene.String(required=True)

    tag = graphene.Field(TagNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        tag = Tag.objects.create(created_by=info.context.user, **input)

        return CreateTag(tag=tag)


class TagMutations(graphene.ObjectType):
    create_tag = CreateTag.Field()


class TagQuery(graphene.ObjectType):
    tag = graphene.relay.Node.Field(TagNode)
    tags = DjangoFilterConnectionField(TagNode)
