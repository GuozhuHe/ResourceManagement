# coding=utf-8
# flake8: noqa
import logging

import tornado
import tornado.web
import tornado.ioloop
import tornado.httpserver
from tornado.options import options, define, parse_command_line

from app.constants import IS_DEBUG
from app.http.urls import url_handlers


def main():
    define(name='port', default=8000, type=int, help='run on the given port')
    parse_command_line()
    logging.info('====== web api server starting at http://0.0.0.0:{} ======'.format(options.port))
    if IS_DEBUG:
        logging.warning('debug mode is enabled!!!')

    app = tornado.web.Application(url_handlers, debug=IS_DEBUG)
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    http_server.start()

    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()
