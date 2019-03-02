# coding: utf-8

from app.http.handlers.base import BaseHandler
from app.utils import get_uniq_id, get_random_string
from app.core.models import (MySQLContainer, RedisContainer)
from app.exceptions import (UnsupportedTypeHTTPError, ResourceNotFoundHTTPError, CreateResourceHTTPError)


class ResourceHandler(BaseHandler):

    def get(self, resource_type, resource_name):
        support_resource = {
            'mysql': MySQLContainer,
            'redis': RedisContainer
        }
        if resource_type.lower() not in support_resource.keys():
            raise UnsupportedTypeHTTPError(reason='Unsupported resource type({type})'.format(type=source_type))

        resource = support_resource[resource_type].get(resource_name)
        if not resource or resource.status == 'exited':
            raise ResourceNotFoundHTTPError(
                reason='Not such resource({type}:{name})'.format(type=resource_type, name=resource_name))

        self.render_json(resource.exposed_info)

    def post(self, resource_type):
        resource_create_func = {
            'mysql': self._create_mysql_resource,
            'redis': self._create_redis_resource,
        }
        if resource_type.lower() not in resource_create_func.keys():
            raise UnsupportedTypeHTTPError(reason='Unsupported resource type({type})'.format(type=resource_type))

        resource = resource_create_func[resource_type]()

        if not resource or resource.status == 'exited':
            raise CreateResourceHTTPError()

        self.render_json(resource.exposed_info)

    def _create_mysql_resource(self):
        character = self.get_argument('character', 'utf8')
        db_name = self.get_argument('dbname', get_random_string())

        resource_name = 'm{}'.format(get_uniq_id())
        # TODO check parameters_dict format
        resource = MySQLContainer.create(
            name=resource_name,
            mysql_user=get_random_string(),
            mysql_user_password=get_random_string(),
            mysql_root_password=get_random_string(),
            mysql_db=db_name,
            parameters_dict={'character': character}
        )

        return resource

    def _create_redis_resource(self):
        db_filename = self.get_argument('dbfilename', 'dump.rdb')
        max_memory = self.get_argument('maxmemory', '1gb')
        append_only = self.get_argument('appendonly', 'yes')
        append_filename = self.get_argument('appendfilename', 'appendonly.aof')

        resource_name = 'r{}'.format(get_uniq_id())
        # TODO check parameters_dict format
        resource = RedisContainer.create(
            name=resource_name,
            parameters_dict={
                'password': get_random_string(),
                'dbfilename': db_filename,
                'maxmemory': max_memory,
                'appendonly': append_only,
                'appendfilename': append_filename
            }
        )

        return resource
