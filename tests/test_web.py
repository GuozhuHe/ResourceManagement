# coding=utf-8
from unittest import mock
from tornado.util import ObjectDict
from tornado.escape import json_decode

from tests.base import BaseWebTestCase


class ResourcesHandlerTestCase(BaseWebTestCase):
    expected_resource = {
        'exposed_info': {
            "resource_id": "5c0d193556259ed8d09bb",
            "resource_name": "r32",
            "server_ip": "172.20.10.5",
            "exposed_port": "32793",
            "db_password": "61VmB9Rh",
            "platform": "linux",
            "status": "running",
            "image_version": "redis:5.0",
            "connect_string": "redis-cli -h 172.20.10.5 -p 32793 -a 61VmB9Rh"
        },
        'status': 'running'
    }

    @mock.patch('app.http.handlers.resource.RedisContainer')
    def test_get(self, mock_container):
        mock_container.get.return_value = ObjectDict(self.expected_resource)
        response = self.fetch_json(url='/api/resources/redis/r32')
        self.assertDictEqual(response, self.expected_resource['exposed_info'])

    @mock.patch('app.http.handlers.resource.RedisContainer')
    def test_get_when_error(self, mock_container):
        # unsupported resource type
        response = self.get(url='/api/resources/mongodb/r32')
        self.assertEqual(response.code, 400)
        self.assertEqual(json_decode(response.body)["error"]["message"], "Unsupported resource type(mongodb)")

        # Not such resource
        mock_container.get.return_value = None
        response = self.get(url='/api/resources/redis/m11')
        self.assertEqual(response.code, 404)
        self.assertEqual(json_decode(response.body)["error"]["message"], "Not such resource(redis:m11)")

    @mock.patch('app.http.handlers.resource.RedisContainer')
    def test_post(self, mock_container):
        mock_container.create.return_value = ObjectDict(self.expected_resource)
        response = self.post(url='/api/resources/redis')
        self.assertEqual(response.code, 200)
        self.assertEqual(json_decode(response.body), self.expected_resource['exposed_info'])

    @mock.patch('app.http.handlers.resource.RedisContainer')
    def test_post_when_error(self, mock_container):
        # unsupported resource type
        response = self.post(url='/api/resources/mongodb')
        self.assertEqual(response.code, 400)
        self.assertEqual(json_decode(response.body)["error"]["message"], "Unsupported resource type(mongodb)")

        # Not such resource
        mock_container.create.return_value = None
        response = self.post(url='/api/resources/redis')
        self.assertEqual(response.code, 500)
        self.assertEqual(json_decode(response.body)["error"]["message"],
                         "Failed to create resource, check your parameters(maybe your parameter format is wrong)")
