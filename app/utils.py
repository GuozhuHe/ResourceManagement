# coding=utf-8
import os
import redis
import random
import socket
import string

REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
REDIS_PORT = os.environ.get('REDIS_PORT', '6379')
redis_instance = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)


def get_uniq_id():
    return redis_instance.incr('db_counter')


def get_host_ip():
    try:
        socket_instance = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        socket_instance.connect(('8.8.8.8', 80))
        ip = socket_instance.getsockname()[0]
    finally:
        socket_instance.close()

    return ip


def list_to_dict(l):
    """['1=a','2=b','3=c'] -> {'1':'a','2':'b','3':'c'}"""
    d = dict()
    for pair in l:
        items = pair.split('=')
        d[items[0]] = items[1]
    return d


def get_line_from_file(file_path, startswith):
    target_line = ''
    with open(file_path, 'r') as file_object:
        for line in file_object.read().split('\n'):
            if line.startswith(startswith):
                target_line = line
                break

    return target_line


def get_random_string(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
