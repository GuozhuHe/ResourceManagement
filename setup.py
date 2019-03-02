#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from setuptools import setup

from app import __version__

# get the dependencies and installs
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'requirements.txt')) as f:
    all_requirements = f.read().split('\n')

setup(
    name='ResourceManagement',
    version=__version__,
    author='heguozhu',
    author_email='heguozhuchn@gmail.com',
    description='Storage resource(MySQL, Redis) management system',
    zip_safe=False,
    install_requires=all_requirements,
    entry_points={
        'console_scripts': [
            'web = app.http.web:main',
        ],
    }
)
