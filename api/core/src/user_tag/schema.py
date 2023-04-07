import graphene
from django.db import models
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from core.src.user_tag.model import UserTag


class UserTagNode(DjangoObjectType):
    class Meta:
        model = UserTag
        interfaces = (graphene.relay.Node,)
        fields = [
            "uid",
            "created_at",
            "updated_at",
            "user",
            "tag",
            "color",
            "description",
            "is_hidden",
        ]
        filter_fields = [
            "uid",
            "created_at",
            "updated_at",
            "user",
            "tag",
            "color",
            "description",
            "is_hidden",
        ]

    def get_queryset(self, queryset, info):
        isnt_deleted = models.Q(is_deleted=False)

        return queryset.filter(isnt_deleted)


class CreateUserTag(graphene.relay.ClientIDMutation):
    class Input:
        tag = graphene.UUID(required=True)
        color = graphene.String()
        description = graphene.String()

    user_tag = graphene.Field(UserTagNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        user_tag = UserTag.objects.create(user=info.context.user, **input)

        return CreateUserTag(user_tag=user_tag)


class UpdateUserTag(graphene.relay.ClientIDMutation):
    class Input:
        uid = graphene.UUID(required=True)
        tag = graphene.UUID()
        color = graphene.String()
        description = graphene.String()

    user_tag = graphene.Field(UserTagNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        user_tag = UserTag.objects.get(uid=input.pop("uid"))
        user_tag.update(**input)

        return UpdateUserTag(user_tag=user_tag)


class DeleteUserTag(graphene.relay.ClientIDMutation):
    class Input:
        uid = graphene.UUID(required=True)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        user_tag = UserTag.objects.get(uid=input.pop("uid"))
        user_tag.update(is_deleted=True)

        return DeleteUserTag(success=True)


class UserTagMutations(graphene.ObjectType):
    create_user_tag = CreateUserTag.Field()
    update_user_tag = UpdateUserTag.Field()
    delete_user_tag = DeleteUserTag.Field()


class UserTagQuery(graphene.ObjectType):
    user_tag = graphene.relay.Node.Field(UserTagNode)
    user_tags = DjangoFilterConnectionField(UserTagNode)
