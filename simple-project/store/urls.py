from django.conf.urls import patterns, url

from .views import template_test

urlpatterns = patterns('',
    # /template_test
    url(
        r'^template_test/(?P<review_id>[0-9]*)$',
        template_test,
        name='template_test',
    ),
)
