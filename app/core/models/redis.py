# coding=utf-8
from app.utils import get_line_from_file
from app.core.models.base import BaseContainer
from app.constants import (REDIS_DATA_PATH, REDIS_CONFIG_PATH, LOCAL_IP, REDIS_CONFIG_TEMPLATE,
                           REDIS_CONTAINER_DATA_PATH, REDIS_CONTAINER_CONFIG_PATH, DockerImage, DockerVolumeMode)


class RedisContainer(BaseContainer):
    image = DockerImage.REDIS
    port = 6379

    @classmethod
    def create(cls, name, parameters_dict):
        # Generate and mount external storage files
        cls.generate_mount_file(
            name=name, data_file_path=REDIS_DATA_PATH, config_file_path=REDIS_CONFIG_PATH,
            config_template=REDIS_CONFIG_TEMPLATE, parameters_dict=parameters_dict
        )
        volume = {}
        volume.update(cls.format_volume_mapping(
            host_path=REDIS_DATA_PATH.format(name=name),
            container_path=REDIS_CONTAINER_DATA_PATH,
            mode=DockerVolumeMode.READ_AND_WRITE)
        )
        volume.update(cls.format_volume_mapping(
            host_path=REDIS_CONFIG_PATH.format(name=name),
            container_path=REDIS_CONTAINER_CONFIG_PATH,
            mode=DockerVolumeMode.READ_ONLY
        ))

        container = cls.client.containers.run(name=name, image=cls.image, volumes=volume,
                                              ports=cls.format_bind_ports(container_port=cls.port, host_ports=None),
                                              command='redis-server ' + REDIS_CONTAINER_CONFIG_PATH,
                                              detach=True)

        return cls(container)

    @property
    def connection_url(self):
        return "redis-cli -h {host} -p {port} -a {password}".format(
            host=LOCAL_IP,
            port=self.exposed_port,
            password=self.password
        )

    @property
    def password(self):
        line = get_line_from_file(REDIS_CONFIG_PATH.format(name=self._container.name), 'requirepass')
        return line.split(' ')[1]

    @property
    def exposed_info(self):
        """ The information that allow exposure to outside"""
        return {
            'resource_id': self._container.id,
            'resource_name': self._container.name,
            'server_ip': LOCAL_IP,
            'exposed_port': self.exposed_port,
            'db_password': self.password,
            'platform': self._container.attrs['Platform'],
            'status': self.status,
            'image_version': self.image,
            'connect_string': self.connection_url,
        }
