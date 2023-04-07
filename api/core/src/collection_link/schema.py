import graphene
from django.db import models
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from core.src.collection_link.model import CollectionLink


class CollectionLinkNode(DjangoObjectType):
    class Meta:
        model = CollectionLink
        interfaces = (graphene.relay.Node,)
        fields = [
            "created_at",
            "updated_at",
            "created_by",
            "link",
            "collection",
            "note",
        ]
        filter_fields = [
            "created_at",
            "updated_at",
            "created_by",
            "link",
            "collection",
            "note",
        ]

    def get_queryset(self, queryset, info):
        isnt_deleted = models.Q(is_deleted=False)
        is_collection_public = models.Q(collection__is_public=True)

        if info.context.user.is_anonymous:
            return queryset.filter(isnt_deleted & is_collection_public)

        is_collection_owner = models.Q(collection__created_by=info.context.user)
        is_owner = models.Q(created_by=info.context.user)
        return queryset.filter(
            isnt_deleted & (is_collection_public | is_collection_owner | is_owner)
        )


class CreateCollectionLink(graphene.relay.ClientIDMutation):
    class Input:
        collection = graphene.UUID(required=True)
        link = graphene.UUID(required=True)
        note = graphene.String()

    collection_link = graphene.Field(CollectionLinkNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        collection_link = CollectionLink.objects.create(
            created_by=info.context.user, **input
        )

        return CreateCollectionLink(collection_link=collection_link)


class UpdateCollectionLink(graphene.relay.ClientIDMutation):
    class Input:
        uid = graphene.UUID(required=True)
        collection = graphene.UUID()
        link = graphene.UUID()
        note = graphene.String()

    collection_link = graphene.Field(CollectionLinkNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        collection_link = CollectionLink.objects.get(uid=input.pop("uid"))
        collection_link.update(**input)

        return UpdateCollectionLink(collection_link=collection_link)


class DeleteCollectionLink(graphene.relay.ClientIDMutation):
    class Input:
        uid = graphene.UUID(required=True)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        collection_link = CollectionLink.objects.get(uid=input.pop("uid"))
        collection_link.update(is_deleted=True)

        return DeleteCollectionLink(success=True)


class CollectionLinkMutations(graphene.ObjectType):
    create_collection_link = CreateCollectionLink.Field()
    update_collection_link = UpdateCollectionLink.Field()
    delete_collection_link = DeleteCollectionLink.Field()


class CollectionLinkQuery(graphene.ObjectType):
    collection_link = graphene.relay.Node.Field(CollectionLinkNode)
    collection_links = DjangoFilterConnectionField(CollectionLinkNode)
