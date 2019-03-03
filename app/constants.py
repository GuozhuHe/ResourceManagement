# coding=utf-8
import os

IS_DEBUG = (os.environ.get('ENV', 'dev') == 'dev')
PROJECT_ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))

REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
REDIS_PORT = os.environ.get('REDIS_PORT', '6379')

# docker config
DOCKER_SERVER_PATH = os.environ.get('DOCKER_PATH', 'unix://var/run/docker.sock')

MYSQL_DATA_PATH = os.path.join(PROJECT_ROOT_DIR, 'docker_data', 'mysql', '{name}', 'data')
MYSQL_CONFIG_PATH = os.path.join(PROJECT_ROOT_DIR, 'docker_data', 'mysql', '{name}', 'my.cnf')
REDIS_DATA_PATH = os.path.join(PROJECT_ROOT_DIR, 'docker_data', 'redis', '{name}', 'data')
REDIS_CONFIG_PATH = os.path.join(PROJECT_ROOT_DIR, 'docker_data', 'redis', '{name}', 'redis.conf')

MYSQL_CONTAINER_DATA_PATH = '/var/lib/mysql'
MYSQL_CONTAINER_CONFIG_PATH = '/etc/mysql/my.cnf'
REDIS_CONTAINER_DATA_PATH = '/data'
REDIS_CONTAINER_CONFIG_PATH = '/etc/redis/redis.conf'


class DockerImage(object):
    MYSQL = 'mysql:5.7'
    REDIS = 'redis:5.0'


class DockerVolumeMode(object):
    READ_ONLY = 'ro'
    READ_AND_WRITE = 'rw'


MYSQL_CONFIG_TEMPLATE = """[client]
default-character-set={character}
[mysqld]
character-set-server={character}
[mysql]
default-character-set={character}"""

REDIS_CONFIG_TEMPLATE = """dbfilename {dbfilename}
maxmemory {maxmemory}
appendonly {appendonly}
appendfilename "{appendfilename}"
requirepass {password}
protected-mode no
port 6379
tcp-backlog 511
timeout 0
tcp-keepalive 300
databases 16
save 900 1
save 300 10
save 60 10000
appendfsync everysec
auto-aof-rewrite-percentage 100
auto-aof-rewrite-min-size 64mb
aof-load-truncated yes
aof-use-rdb-preamble yes
slowlog-max-len 128
aof-rewrite-incremental-fsync yes
rdb-save-incremental-fsync yes"""
# docker config end
