#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

# Hack to prevent "TypeError: 'NoneType' object is not callable" error
# in multiprocessing/util.py _exit_function when running `python
# setup.py test`
# (see http://www.eby-sarna.com/pipermail/peak/2010-May/003357.html)
for m in ('multiprocessing', 'billiard'):
    try:
        __import__(m)
    except ImportError:
        pass

setup(
    # Package information
    name='repi-server',
    version='0.2',
    author='Fabian Kochem',
    author_email='fkochem@gmail.com',
    url='http://github.com/vortec/repi-server',
    description='RePi server, a Redis PubSub interface for PyPi.',
    license='MIT',

    # Dependencies
    install_requires=[
        'redis',
        'tornado',
        'tornado-redis'
    ],

    # Entry points
    entry_points={
        'console_scripts': ['repi-server=repi_server.command_line:main']
    },

    # PyPi-related metadata
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2.7',
        'Topic :: System :: Software Distribution'
    ]
)
