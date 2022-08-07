# Listany - Copyright (C) 2022  Thalida Noel
import email
from django.test import TestCase
import graphene
from bookmarks.models import Link
from bookmarks.schema import BookmarkQuery, LinkNode
from users.models import User


class BookmarkLinkTestCase(TestCase):
    def setUp(self):
        test_user = User.objects.create(
            email="user@test.com", username="test_user")

        Link.objects.create(
            url="https://foo.bar",
            is_auto_fetch_enabled=False,
            curated_by=test_user
        )

    def test_bookmark__link_query(self):
        query = """
            query BookmarkQuery {
                allLinks {
                    edges {
                        node {
                            url
                        }
                    }
                }
            }
        """
        expected = {
            'allLinks': {
                'edges': [
                    {
                        'node': {
                            'url': 'https://foo.bar'
                        }
                    }
                ]
            }
        }
        schema = graphene.Schema(query=BookmarkQuery)
        result = schema.execute(query)
        assert not result.errors
        assert result.data == expected
