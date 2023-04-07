import graphene
from django.db import models
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from core.src.link.model import Link


class LinkNode(DjangoObjectType):
    class Meta:
        model = Link
        interfaces = (graphene.relay.Node,)
        fields = [
            "uid",
            "created_at",
            "updated_at",
            "url",
            "title",
            "description",
            "is_hidden",
        ]
        filter_fields = [
            "uid",
            "created_at",
            "updated_at",
            "url",
            "title",
            "description",
            "is_hidden",
        ]

    def get_queryset(self, queryset, info):
        isnt_deleted = models.Q(is_deleted=False)

        return queryset.filter(isnt_deleted)


class CreateLink(graphene.relay.ClientIDMutation):
    class Input:
        url = graphene.String(required=True)
        title = graphene.String()
        description = graphene.String()

    link = graphene.Field(LinkNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        link = Link.objects.create(
            created_by=info.context.user,
            **input,
        )

        return CreateLink(link=link)


class LinkMutations(graphene.ObjectType):
    create_link = CreateLink.Field()


class LinkQuery(graphene.ObjectType):
    link = graphene.relay.Node.Field(LinkNode)
    links = DjangoFilterConnectionField(LinkNode)
