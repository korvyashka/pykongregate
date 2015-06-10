from unittest import TestCase

from mock import patch

from pykongregate.api import _handle_request
from pykongregate.exceptions import NullResponseException


class TestApi(TestCase):

    def test_base_request(self):
        with patch('requests.get') as patch_get:
            class _Temp(object):
                def __init__(self):
                    self.text = ''

            patch_get.side_effect = [_Temp()]
            url = 'www.example.com'
            self.assertRaises(
                NullResponseException,
                _handle_request,
                url, {},
            )
        with patch('requests.get') as patch_get:
            class _Temp(object):
                def __init__(self):
                    self.text = '{"hello_world": "hello_world"}'

            patch_get.side_effect = [_Temp()]
            url = 'www.example.com'
            params = {}
            response = _handle_request(url, params)

            self.assertEqual(
                response, {"hello_world": "hello_world"}
            )

