# coding=utf-8
from app.core.models.base import BaseContainer
from app.constants import (MYSQL_CONFIG_PATH, MYSQL_DATA_PATH, LOCAL_IP, MYSQL_CONFIG_TEMPLATE,
                           MYSQL_CONTAINER_DATA_PATH, MYSQL_CONTAINER_CONFIG_PATH, DockerImage, DockerVolumeMode)


class MySQLContainer(BaseContainer):
    image = DockerImage.MYSQL
    port = 3306

    @classmethod
    def create(cls, name, mysql_user, mysql_user_password, mysql_root_password, mysql_db, parameters_dict):
        environment = {
            'MYSQL_USER': mysql_user,
            'MYSQL_PASSWORD': mysql_user_password,
            'MYSQL_ROOT_PASSWORD': mysql_root_password,
            'MYSQL_DATABASE': mysql_db
        }

        # Generate and mount external storage files
        cls.generate_mount_file(name=name, data_file_path=MYSQL_DATA_PATH, config_file_path=MYSQL_CONFIG_PATH,
                                config_template=MYSQL_CONFIG_TEMPLATE, parameters_dict=parameters_dict)
        volume = {}
        volume.update(cls.format_volume_mapping(
            host_path=MYSQL_DATA_PATH.format(name=name),
            container_path=MYSQL_CONTAINER_DATA_PATH,
            mode=DockerVolumeMode.READ_AND_WRITE
        ))
        volume.update(cls.format_volume_mapping(
            host_path=MYSQL_CONFIG_PATH.format(name=name),
            container_path=MYSQL_CONTAINER_CONFIG_PATH,
            mode=DockerVolumeMode.READ_ONLY
        ))

        container = cls.client.containers.run(name=name, image=cls.image, environment=environment, volumes=volume,
                                              ports=cls.format_bind_ports(container_port=cls.port, host_ports=None),
                                              detach=True)

        return cls(container)

    @property
    def connection_url(self):
        return "mysql -h {host} -P {port} -u {username} -D {db_name} -p{password}". \
            format(username=self.env['MYSQL_USER'],
                   password=self.env['MYSQL_PASSWORD'],
                   host=LOCAL_IP,
                   port=self.exposed_port,
                   db_name=self.env['MYSQL_DATABASE'])

    @property
    def exposed_info(self):
        """ The information that allow exposure to outside"""
        return {
            'resource_id': self._container.id,
            'resource_name': self._container.name,
            'server_ip': LOCAL_IP,
            'exposed_port': self.exposed_port,
            'db_name': self.env['MYSQL_DATABASE'],
            'db_username': self.env['MYSQL_USER'],
            'db_password': self.env['MYSQL_PASSWORD'],
            'platform': self._container.attrs['Platform'],
            'status': self.status,
            'image_version': self.image,
            'connect_string': self.connection_url,
        }
