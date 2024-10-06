# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='pgman',
    version='0.0.6',
    description='Python操作PostgreSQL',
    url='https://github.com/markadc/wauo',
    author='WangTuo',
    author_email='markadc@126.com',
    packages=find_packages(),
    license='MIT',
    zip_safe=False,
    install_requires=['psycopg2', 'fake_useragent', 'loguru'],
    keywords=['Python', 'DB', 'PostgreSQL'],
    long_description=long_description,
    long_description_content_type='text/markdown'
)
