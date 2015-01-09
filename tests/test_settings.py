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
        # # Uncomment to test with a sqlite3 database, otherwise test in memory
        # 'TEST': {
        #     'ENGINE': 'django.db.backends.sqlite3',
        #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        # }
    }
}


DJANGO_REVIEWS = {}
DJANGO_REVIEWS['UPDATED_COMPARISON_SECONDS'] = 1
DJANGO_REVIEWS['MAX_SCORE'] = 5
DJANGO_REVIEWS['MIN_SCORE'] = 1
DJANGO_REVIEWS['COMMENT_APPROVAL_REQUIRED'] = True
