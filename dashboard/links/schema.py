import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from links.models import Link, Collection


class LinkNode(DjangoObjectType):
    pk = graphene.Field(type=graphene.UUID, source='id')

    class Meta:
        model = Link
        filter_fields = {
            'url': ['exact', 'icontains', 'istartswith'],
            'collections': ['exact', 'icontains', 'istartswith'],
        }
        interfaces = (graphene.relay.Node, )

    def resolve_icon(self, info):
        has_icon = self.icon and self.icon.name
        return f"{self.icon.url}" if has_icon else None

    def resolve_image(self, info):
        has_image = self.image and self.image.name
        return f"{self.image.url}" if has_image else None


class CollectionNode(DjangoObjectType):
    pk = graphene.Field(type=graphene.UUID, source='id')

    class Meta:
        model = Collection
        filter_fields = {
            'name': ['exact', 'icontains', 'istartswith'],
            'slug': ['exact', 'icontains', 'istartswith'],
        }
        interfaces = (graphene.relay.Node, )


class CreateLink(graphene.relay.ClientIDMutation):
    class Input:
        url = graphene.String(required=True)
        collections = graphene.List(graphene.ID, default_value=[])

    link = graphene.Field(LinkNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **data):
        link = Link.objects.create(
            url=data.get('url'),
            created_by=info.context.user,
        )
        # link.collections.set(Collection.objects.filter(
        #     id__in=data.get('collections')
        # ))
        for collection_id in data.get('collections'):
            collection = Collection.objects.get(id=collection_id)
            link.collections.add(collection)

        link.save()

        return CreateLink(link=link)


class DeleteLink(graphene.relay.ClientIDMutation):
    class Input:
        id = graphene.ID()

    link = graphene.Field(LinkNode)
    success = graphene.Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **data):
        link = Link.objects.get(
            pk=data.get('id'),
            created_by=info.context.user
        )

        link.delete()

        return DeleteLink(link=link, success=True)


class CreateCollection(graphene.relay.ClientIDMutation):
    class Input:
        name = graphene.String(required=True)
        description = graphene.String(default_value=None)

    collection = graphene.Field(CollectionNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **data):
        collection = Collection.objects.create(
            name=data.get('name'),
            description=data.get('description'),
            created_by=info.context.user,
        )
        collection.save()

        return CreateCollection(collection=collection)


class DeleteCollection(graphene.relay.ClientIDMutation):
    class Input:
        id = graphene.ID()

    collection = graphene.Field(CollectionNode)
    success = graphene.Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **data):
        collection = Collection.objects.get(
            pk=data.get('id'),
            created_by=info.context.user
        )

        collection.delete()

        return DeleteCollection(collection=collection, success=True)


class LinkQuery(graphene.ObjectType):
    link = graphene.relay.Node.Field(LinkNode)
    all_links = DjangoFilterConnectionField(LinkNode)

    collection = graphene.relay.Node.Field(CollectionNode)
    all_collections = DjangoFilterConnectionField(CollectionNode)


class LinkMutation(graphene.ObjectType):
    create_link = CreateLink.Field()
    delete_link = DeleteLink.Field()

    create_collection = CreateCollection.Field()
    delete_collection = DeleteCollection.Field()
