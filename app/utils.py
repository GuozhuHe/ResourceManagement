# coding=utf-8
import redis
import random
import string
import requests

from app.constants import (REDIS_PORT, REDIS_HOST)

redis_instance = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)


def get_uniq_id():
    return redis_instance.incr('db_counter')


def get_public_ip():
    response = requests.get('https://ifconfig.co/json')
    assert requests.status_codes == 200
    response_content = response.json()
    assert 'ip' in response_content
    return response_content['ip']


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
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))
