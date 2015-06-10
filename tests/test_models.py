from unittest import TestCase

from mock import patch

from pykongregate.exceptions import ApiException
from pykongregate import KongApi, KongUser


class TestModels(TestCase):

    def setUp(self):
        self.patch_response = patch('pykongregate.api._handle_request')
        self.patched = self.patch_response.start()

    def tearDown(self):
        self.patch_response.stop()

    def set_response(self, response_object):
        self.patched.side_effect = [response_object]

    def test_get_items(self):
        api = KongApi('')
        mocked_response = {
            "items": [
                {
                    "description": "first_item",
                    "game_id": 1,
                    "game_title": "title1",
                    "id": 1,
                    "identifier": "product_id_1",
                    "image_url": "http://example.com/example.png",
                    "name": "first_item",
                    "price": 5,
                    "tags": []
                },
                {
                    "description": "second_item",
                    "game_id": 2,
                    "game_title": "title2",
                    "id": 2,
                    "identifier": "product_id_2",
                    "image_url": "http://example.com/example.png",
                    "name": "second_item",
                    "price": 5,
                    "tags": []
                },
            ],
            "success": True
        }

        self.set_response(mocked_response)
        items = api.get_items()
        self.assertEqual(2, len(items))
        item1 = items[0]
        self.assertEqual(item1.id, 1)

    def test_api_exception(self):
        api = KongApi('')
        mocked_response = {
            'success': False,
            'error_description': 'desc'
        }
        self.set_response(mocked_response)
        self.assertRaises(
            ApiException,
            api.get_items
        )

    def test_get_user_info(self):
        api = KongApi('')
        mocked_response = {
            "friend_ids": [],
            "friends": [],
            "muted_user_ids": [],
            "muted_users": [],
            "num_pages": 1,
            "page_num": 1,
            "private": False,
            "success": True,
            "user_id": 1,
            "user_vars": {
                "admin": False,
                "age": 18,
                "avatar_url": "http://example.com/example.png",
                "chat_avatar_url": "http://example.com/example.png",
                "developer": False,
                "game_title": "game_title",
                "game_url": "http://www.kongregate.com/games/example/example",
                "gender": "Male",
                "level": 1,
                "moderator": False,
                "points": 1,
                "username": "username"
            },
            "username": "username"
        }
        self.set_response(mocked_response)
        response = api.get_user_info('test_user')
        self.assertEqual(response, mocked_response)

    def test_has_item(self):
        user = KongUser('', user_id=1111)

        mocked_response = {
            "items": [
                {
                    "data": None,
                    "description": "item_desc1",
                    "id": 1,
                    "identifier": "product_id_1",
                    "name": "item_name1",
                    "remaining_uses": 1
                },
                {
                    "data": None,
                    "description": "item_desc2",
                    "id": 2,
                    "identifier": "product_id_2",
                    "name": "item_name1",
                    "remaining_uses": 2
                }
            ],
            "s": "base64string",
            "signature": "signature",
            "success": True
        }

        self.set_response(mocked_response)
        items = user.items()
        self.assertEqual(2, len(items))

        self.assertTrue(user.has_item(id=1, refetch=False))
        self.assertTrue(user.has_item(id=2, refetch=False))
        self.assertFalse(user.has_item(id=3, refetch=False))
        self.assertTrue(user.has_item(identifier='product_id_2', refetch=False))
        self.assertFalse(user.has_item(identifier='product_id_3', refetch=False))
        self.assertTrue(user.has_item(id=2, identifier='product_id_2', refetch=False))
        self.assertFalse(user.has_item(id=1, identifier='product_id_2', refetch=False))
        self.assertFalse(user.has_item(id=3, identifier='product_id_3', refetch=False))
        self.assertFalse(user.has_item(id=2, identifier='product_id_3', refetch=False))


