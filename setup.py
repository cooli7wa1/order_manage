# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='order_manage',
    version='0.1.0',
    description='Record in & out orders',
    long_description=readme,
    author='Rickey Liu',
    author_email='liuqi@microtrust.com.cn',
    url='git@github.com:cooli7wa/order_manage.git',
    license=license,
    packages=find_packages(exclude=('tests', 'docs', 'tools'))
)

