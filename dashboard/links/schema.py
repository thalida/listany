import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from links.models import Link, Collection


class LinkNode(DjangoObjectType):
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
    class Meta:
        model = Collection
        filter_fields = {
            'name': ['exact', 'icontains', 'istartswith'],
            'slug': ['exact', 'icontains', 'istartswith'],
        }
        interfaces = (graphene.relay.Node, )


class LinkInput(graphene.InputObjectType):
    id = graphene.ID()
    url = graphene.String()
    title = graphene.String(default_value=None)
    description = graphene.String(default_value=None)
    image = graphene.String(default_value=None)
    collections = graphene.List(graphene.ID, default_value=[])
    created_by = graphene.ID()


class CreateLink(graphene.Mutation):
    link = graphene.Field(LinkNode)

    class Arguments:
        link_data = LinkInput(required=True)

    @staticmethod
    def mutate(info, link_data):
        link = Link.objects.create(
            url=link_data.url,
            title=link_data.title,
            description=link_data.description,
            image=link_data.image,
            created_by=info.context.user,
        )
        link.collections.set(link_data.collections)
        link.save()

        return CreateLink(link=link)


class LinkQuery(graphene.ObjectType):
    link = graphene.relay.Node.Field(LinkNode)
    all_links = DjangoFilterConnectionField(LinkNode)

    collection = graphene.relay.Node.Field(CollectionNode)
    all_collections = DjangoFilterConnectionField(CollectionNode)


class LinkMutation(graphene.ObjectType):
    create_link = CreateLink.Field()
