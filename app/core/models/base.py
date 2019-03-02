# coding=utf-8
import os
import docker
from docker.models.containers import Container
from docker.errors import NotFound

from app.utils import list_to_dict
from app.exceptions import ContainerException
from app.constants import (DOCKER_SERVER_PATH, DockerVolumeMode)

docker_client = docker.DockerClient(base_url=DOCKER_SERVER_PATH)


class BaseContainer(object):
    client = docker_client
    port = None
    image = None

    def __init__(self, container):
        if type(container) is not Container:
            raise ValueError('Parameter(container) must be an instance of docker.models.containers.Container')
        self._container = container

    @classmethod
    def create(cls, *args, **kwargs):
        raise NotImplementedError

    @classmethod
    def get(cls, short_id):
        try:
            container = cls.client.containers.get(container_id=short_id)
            if cls.is_same_type_image(cls.image, container.attrs['Config']['Image']):
                return cls(container)
        except NotFound:
            return None

    def exec(self, command, *args, **kwargs):
        if not self._container:
            raise ContainerException("Container should be started before exec")
        return self._container.exec_run(command=command, *args, **kwargs)

    @property
    def inspect_info(self):
        return self.client.api.inspect_container(container=self._container.short_id)

    @property
    def env(self):
        return list_to_dict(self._container.attrs['Config']['Env'])

    @property
    def short_id(self):
        return self._container.short_id

    @property
    def exposed_port(self):
        if not self.port:
            raise AttributeError('Container does not have a port set')
        return self.client.api.port(self.short_id, self.port)[0]['HostPort']

    @property
    def status(self):
        return self.inspect_info['State']['Status']

    @staticmethod
    def format_bind_ports(container_port, host_ports, protocol='tcp'):
        """
        ports format:
        {'2222/tcp': 3333}
        {'2222/tcp': None}
        {'1111/tcp': ('127.0.0.1', 1111)}
        {'1111/tcp': [1234, 4567]}
        """
        return {'{container_port}/{protocol}'.format(container_port=container_port, protocol=protocol): host_ports}

    @staticmethod
    def format_volume_mapping(host_path, container_path, mode=DockerVolumeMode.READ_ONLY):
        """ '~/usr/local/etc/mysql/my.cnf': {'bind': '/etc/mysql/my.cnf', 'mode': 'ro'}"""
        if mode not in (DockerVolumeMode.READ_ONLY, DockerVolumeMode.READ_AND_WRITE):
            raise ValueError("Unsupported docker volume mode")
        return {host_path: {'bind': container_path, 'mode': mode}}

    @classmethod
    def generate_mount_file(cls, name, data_file_path, config_file_path, config_template, parameters_dict=None):
        """ generate container mount data dir and config file if not exist """
        data_file_path = data_file_path.format(name=name)
        config_file_path = config_file_path.format(name=name)

        os.makedirs(data_file_path, exist_ok=True)

        with open(config_file_path, 'w') as file_object:
            file_object.write(config_template.format(**parameters_dict))

    @classmethod
    def is_same_type_image(cls, image1, image2):
        """
        is_same_type_image('mysql:5.0', 'mysql:lastest') -> True
        is_same_type_image('mysql:5.0', 'redis:4.0') -> False
        :return:
        """
        if not image1 or not image2:
            return False
        return image1.split(':')[0] == image2.split(':')[0]

    @property
    def exposed_info(self):
        """ The information that allow exposure to outside"""
        raise NotImplementedError
