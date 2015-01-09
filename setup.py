#!/usr/bin/env python

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

requirements = [
    'django>=1.6,<2.0',
]

test_requirements = [
    'factory-boy>=2.4,<3.0',
]


setup(
    name='django-reviews',
    version='1.0',
    description='A simple to use framework for user submitted reviews of objects.',
    author='Austin Heiman',
    author_email='atheimanksu@gmail.com',
    url='https://github.com/atheiman/django-reviews',
    packages=find_packages(),
    package_dir={'reviews':
                 'reviews'},
    install_requires=requirements,
    tests_requires=requirements + test_requirements,
)
