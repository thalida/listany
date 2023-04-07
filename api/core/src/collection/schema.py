import graphene
from django.db import models
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from core.src.collection.model import Collection


class CollectionNode(DjangoObjectType):
    class Meta:
        model = Collection
        interfaces = (graphene.relay.Node,)
        fields = [
            "uid",
            "created_at",
            "updated_at",
            "created_by",
            "title",
            "subtitle",
            "description",
            "links",
            "tags",
            "is_public",
            "is_hidden",
        ]
        filter_fields = [
            "uid",
            "created_at",
            "updated_at",
            "created_by",
            "title",
            "subtitle",
            "description",
            "links",
            "tags",
            "is_public",
            "is_hidden",
        ]

    def get_queryset(self, queryset, info):
        isnt_deleted = models.Q(is_deleted=False)
        is_public = models.Q(is_public=True)
        if info.context.user.is_anonymous:
            return queryset.filter(isnt_deleted & is_public)

        is_owner = models.Q(created_by=info.context.user)
        return queryset.filter(isnt_deleted & (is_public | is_owner))


class CreateCollection(graphene.relay.ClientIDMutation):
    class Input:
        title = graphene.String(required=True)
        subtitle = graphene.String()
        description = graphene.String()
        is_public = graphene.Boolean()
        tags = graphene.List(graphene.UUID)

    collection = graphene.Field(CollectionNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        collection = Collection.objects.create(created_by=info.context.user, **input)

        return CreateCollection(collection=collection)


class UpdateCollection(graphene.relay.ClientIDMutation):
    class Input:
        uid = graphene.UUID(required=True)
        title = graphene.String()
        subtitle = graphene.String()
        description = graphene.String()
        is_public = graphene.Boolean()
        is_hidden = graphene.Boolean()
        tags = graphene.List(graphene.UUID)

    collection = graphene.Field(CollectionNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        collection = Collection.objects.get(uid=input.pop("uid"))
        collection.update(**input)

        return UpdateCollection(collection=collection)


class DeleteCollection(graphene.relay.ClientIDMutation):
    class Input:
        uid = graphene.UUID(required=True)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        collection = Collection.objects.get(uid=input.pop("uid"))
        collection.update(is_deleted=True)

        return DeleteCollection(success=True)


class CollectionMutations(graphene.ObjectType):
    create_collection = CreateCollection.Field()
    update_collection = UpdateCollection.Field()
    delete_collection = DeleteCollection.Field()


class CollectionQuery(graphene.ObjectType):
    collection = graphene.relay.Node.Field(CollectionNode)
    collections = DjangoFilterConnectionField(CollectionNode)
