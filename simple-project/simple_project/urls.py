from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'simple_project.views.home', name='home'),
    url(r'^store/', include('store.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
