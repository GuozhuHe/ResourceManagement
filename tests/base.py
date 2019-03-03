#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import logging
from urllib.parse import urlencode
from tornado.testing import AsyncHTTPTestCase
from tornado.escape import json_encode, json_decode

from app.http.web import make_web_app

here_dir = os.path.dirname(__file__)


class BaseWebTestCase(AsyncHTTPTestCase):
    def get_app(self):
        return make_web_app()

    def request(self, method, url, headers=None, data=None, json=None, form=None, **kwargs):
        if not headers:
            headers = {}

        if json is not None:
            headers['Content-Type'] = 'application/json'
            data = json_encode(json)

        elif form is not None:
            headers['Content-Type'] = 'application/x-www-form-urlencoded'
            data = urlencode(form)

        response = self.fetch(url, method=method, headers=headers, body=data, allow_nonstandard_methods=True,
                              **kwargs)

        if response.code / 100 != 2:
            logging.error(response.body)

        return response

    def get(self, url, **kwargs):
        return self.request(url=url, method="GET", **kwargs)

    def post(self, url, **kwargs):
        return self.request(url=url, method="POST", **kwargs)

    def put(self, url, **kwargs):
        return self.request(url=url, method="PUT", **kwargs)

    def fetch_json(self, url, **kwargs):
        response = self.request('GET', url, **kwargs)
        if response.code / 100 != 2:
            raise ValueError('fetch json expect http code 2xx, got {}'.format(response.code))
        return json_decode(response.body)
