# coding=utf-8
from tornado.web import URLSpec

from app.http.handlers import ResourceHandler

url_handlers = [
    # eg: post /api/resources/mysql
    URLSpec(r"/api/resources/(\w+)", ResourceHandler),
    # eg: get /api/resources/mysql/m1
    URLSpec(r"/api/resources/(\w+)/(\w+)", ResourceHandler),
]
