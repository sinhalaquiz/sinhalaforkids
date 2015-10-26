from django.conf.urls import patterns, include, url

urlpatterns = patterns('alphabet.views',
    url(r'^$', 'index'),
    url(r'^lesson/(?P<id>.+)$', 'lesson'),
    url(r'^review/(?P<id>.+)$', 'review'),
)

