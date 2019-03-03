# coding=utf-8
from tornado.web import HTTPError

__all__ = ['UnsupportedTypeHTTPError', 'ResourceNotFoundHTTPError', 'CreateResourceHTTPError']


class BaseHTTPError(HTTPError):
    STATUS_CODE = 500
    REASON = u''

    def __init__(self, status_code=None, reason='', *args, **kwargs):
        super().__init__(
            status_code=status_code if status_code else self.STATUS_CODE,
            reason=reason if reason else self.REASON,
            *args, **kwargs
        )


class UnsupportedTypeHTTPError(BaseHTTPError):
    STATUS_CODE = 400
    REASON = u'Unsupported resource type'


class ResourceNotFoundHTTPError(BaseHTTPError):
    STATUS_CODE = 404
    REASON = u'Not such resource'


class CreateResourceHTTPError(BaseHTTPError):
    STATUS_CODE = 500
    REASON = u'Failed to create resource, check your parameters(maybe your parameter format is wrong)'
