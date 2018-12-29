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

    packages=find_packages('src'),  # include all packages under src
    package_dir={'': 'src'},   # tell setuptools packages are under src
    # 自动包含包内数据文件, include everything in source control
    # include_package_data=True,
    # 安装时，指定包内需要包含的数据文件, 只能包括package内的
    package_data={
        'commvault': ['template/*.json']
    },
    # 指定安装到哪
    data_files=[
        ('', ['src/logging.yaml', 'src/system_config.yaml'])
    ],
    platforms="any",
    py_modules=['commander'],
    # 需要安装的依赖包
    install_requires=['PyYAML', 'requests', 'openpyxl'],

    # scripts 参数是一个 list，安装包时在该参数中列出的文件会被安装到系统 PATH 路径下, 安装时需要执行的脚本列表
    # scripts=[],

    entry_points={
        'console_scripts': [
            'cvctl = commander:main'
        ]
    },
    zip_safe=False
)

