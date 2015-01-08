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


import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# DJANGO_REVIEWS = {}
# DJANGO_REVIEWS['MAX_SCORE'] = 5
# DJANGO_REVIEWS['MIN_SCORE'] = 1
# DJANGO_REVIEWS['SCORE_CHOICES'] = zip(
#     range(DJANGO_REVIEWS['MIN_SCORE'], DJANGO_REVIEWS['MAX_SCORE'] + 1),
#     range(DJANGO_REVIEWS['MIN_SCORE'], DJANGO_REVIEWS['MAX_SCORE'] + 1)
# )
# DJANGO_REVIEWS['MAX_COMMENT_LENGTH'] = 1000,
# DJANGO_REVIEWS['UPDATED_COMPARISON_SECONDS'] = 3
# DJANGO_REVIEWS['AVG_SCORE_DIGITS'] = 2
