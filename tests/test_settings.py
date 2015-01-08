"""Settings to be used for testing django-reviews."""

# Required to run django app:
SECRET_KEY = 'some-bogus-key'
# Required to suppress annoying warning:
MIDDLEWARE_CLASSES = ()


INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'reviews',
    'tests',
]


TEST_RUNNER_VERBOSITY = 1


import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'TEST': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
}


DJANGO_REVIEWS = {}
DJANGO_REVIEWS['UPDATED_COMPARISON_SECONDS'] = 1
