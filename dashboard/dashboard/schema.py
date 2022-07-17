# cookbook/schema.py
import graphene
from graphene_django import DjangoObjectType, DjangoListField
from links.models import Link, Collection


class LinkType(DjangoObjectType):
    class Meta:
        model = Link
        fields = "__all__"


class CollectionType(DjangoObjectType):
    class Meta:
        model = Collection
        fields = "__all__"


class LinkInput(graphene.InputObjectType):
    id = graphene.ID()
    url = graphene.String()


class Query(graphene.ObjectType):
    all_links = graphene.List(LinkType)
    link = graphene.Field(LinkType, link_id=graphene.Int())

    all_link_collections = graphene.List(CollectionType)
    collection = graphene.Field(
        CollectionType,
        collection_id=graphene.Int()
    )
    collection_by_slug = graphene.Field(
        CollectionType,
        slug=graphene.String(required=True)
    )

    def resolve_all_links(self, info, **kwargs):
        return Link.objects.prefetch_related("collections").all()

    def resolve_link(self, info, link_id):
        return Link.objects.prefetch_related("collections").get(pk=link_id)

    def resolve_all_link_collections(self, info, **kwargs):
        return Collection.objects.prefetch_related("links").all()

    def resolve_collection(self, info, collection_id):
        return Collection.objects.prefetch_related("links").get(pk=collection_id)

    def resolve_collection_by_slug(self, info, slug):
        return Collection.objects.prefetch_related("links").get(slug=slug)


schema = graphene.Schema(query=Query)
