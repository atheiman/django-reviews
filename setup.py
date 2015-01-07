#!/usr/bin/env python

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

requirements = [
    'django>=1.6,<2.0',
]


setup(
    name='django-reviews',
    version='1.0',
    description='Django abstract base classes for creating a reviews application',
    author='Austin Heiman',
    author_email='atheimanksu@gmail.com',
    url='https://github.com/atheiman/django-reviews',
    packages=find_packages(),
    package_dir={'reviews':
                 'reviews'},
    install_requires=requirements,
)
