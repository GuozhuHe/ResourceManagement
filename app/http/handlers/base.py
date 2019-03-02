# coding: utf-8
import traceback
from tornado.escape import json_encode
from tornado.web import RequestHandler


class BaseHandler(RequestHandler):

    def render_json(self, data):
        self.set_header('Content-Type', 'application/json')
        self.finish(json_encode(data))

    def write_error(self, status_code, **kwargs):
        error_return = {
            'code': status_code,
            'message': self._reason,
        }
        if self.settings.get("serve_traceback") and "exc_info" in kwargs:
            # in debug mode, try to send a traceback
            lines = []
            for line in traceback.format_exception(*kwargs["exc_info"]):
                lines.append(line)
            error_return['traceback'] = lines

        self.render_json({'error': error_return})
