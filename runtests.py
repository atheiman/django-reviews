#!/usr/bin/env python

"""
Running tests with a standalone Django app without manage.py is complicated. I have done it before (https://github.com/kstateome/dc-affirm/blob/master/runtests.py), but it is complicated.

Running tests with ContentType models is complicated. It tends to not work with the test database ("OperationalError: no such table found").

Running tests with abstract base class Django models is complicated. You have to subclass the model in your tests.



As a result of these struggles, I am trying to simplify by following this example: https://docs.djangoproject.com/en/1.7/topics/testing/advanced/#using-the-django-test-runner-to-test-reusable-applications.

And if that doesn't work I will create a script here that manually compares things with:
    if a != b:
        raise Exception("This test failed.")
"""

import os
import sys

import django
from django.conf import settings
from django.test.utils import get_runner

if __name__ == "__main__":
    os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.test_settings'
    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=2)
    print '\nusing test runner: %s\n' % str(test_runner)
    failures = test_runner.run_tests(["tests"])
    sys.exit(bool(failures))
