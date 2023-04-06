import graphene

from core.src.collection.schema import CollectionMutations, CollectionQuery
from core.src.collection_link.schema import CollectionLinkMutations, CollectionLinkQuery
from core.src.link.schema import LinkMutations, LinkQuery
from core.src.tag.schema import TagMutations, TagQuery
from core.src.user_tag.schema import UserTagMutations, UserTagQuery


class CoreQuery(
    CollectionQuery,
    CollectionLinkQuery,
    LinkQuery,
    TagQuery,
    UserTagQuery,
    graphene.ObjectType
):
    pass


class CoreMutation(
    CollectionMutations,
    CollectionLinkMutations,
    LinkMutations,
    TagMutations,
    UserTagMutations,
    graphene.ObjectType
):
    pass
