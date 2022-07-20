import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from bookmarks.models import Bookmark, Link, Collection


class BookmarkNode(DjangoObjectType):
    pk = graphene.Field(type=graphene.UUID, source='id')

    class Meta:
        model = Bookmark
        filter_fields = {
            'link__url': ['exact', 'icontains', 'istartswith'],
            'collections__name': ['exact', 'icontains', 'istartswith'],
        }
        interfaces = (graphene.relay.Node, )


class LinkNode(DjangoObjectType):
    pk = graphene.Field(type=graphene.UUID, source='id')

    class Meta:
        model = Link
        filter_fields = {
            'url': ['exact', 'icontains', 'istartswith'],
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


class CreateBookmark(graphene.relay.ClientIDMutation):
    class Input:
        url = graphene.String(required=True)
        collections = graphene.List(graphene.ID, default_value=[])

    bookmark = graphene.Field(BookmarkNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **data):
        link, _ = Link.objects.get_or_create(
            url=data.get('url'),
            curated_by=info.context.user,
        )
        bookmark = Bookmark(
            created_by=info.context.user,
            link=link,
        )
        collections = Collection.objects.filter(
            id__in=data.get('collections')
        )
        bookmark.collections.set(collections)
        bookmark.save()

        return CreateBookmark(bookmark=bookmark)


class DeleteBookmark(graphene.relay.ClientIDMutation):
    class Input:
        id = graphene.ID()

    bookmark = graphene.Field(BookmarkNode)
    success = graphene.Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **data):
        bookmark = Bookmark.objects.get(
            pk=data.get('id'),
            created_by=info.context.user
        )

        bookmark.delete()

        return DeleteBookmark(bookmark=bookmark, success=True)


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


class BookmarkQuery(graphene.ObjectType):
    bookmark = graphene.relay.Node.Field(BookmarkNode)
    all_bookmarks = DjangoFilterConnectionField(BookmarkNode)

    link = graphene.relay.Node.Field(LinkNode)
    all_links = DjangoFilterConnectionField(LinkNode)

    collection = graphene.relay.Node.Field(CollectionNode)
    all_collections = DjangoFilterConnectionField(CollectionNode)


class BookmarkMutation(graphene.ObjectType):
    create_bookmark = CreateBookmark.Field()
    delete_bookmark = DeleteBookmark.Field()

    create_collection = CreateCollection.Field()
    delete_collection = DeleteCollection.Field()
