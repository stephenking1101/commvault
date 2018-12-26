# !/usr/bin/env python
# -*- coding:utf-8 -*-

from setuptools import setup, find_packages

setup(
    name="CommvaultCommander",
    version="0.1",
    keywords=("commvault", "restfull", "command"),
    description="Command line tool of Commvault API",
    long_description="Command line tool of Commvault API",
    license="GPL",

    url="http://documentation.commvault.com",
    author="Stephen",
    author_email="stephenwang@commvault.com",

    packages=find_packages(),
    #include_package_data=True,
    platforms="any",
    install_requires=[],

    # scripts 参数是一个 list，安装包时在该参数中列出的文件会被安装到系统 PATH 路径下
    scripts=[],
    package_data={
        '': ['logging.yaml']
    },
    entry_points={
        'console_scripts': [
            'cvctl = commander:main'
        ]
    }
)

