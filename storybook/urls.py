from django.conf.urls import patterns, include, url

urlpatterns = patterns('storybook.views',
    url(r'^$',                                                      'index'),
    url(r'^index$',                                                 'index'),
    url(r'^title/(?P<story>\d+)$',                                  'title'),
    url(r'^read/(?P<story>\d+)/(?P<section>\d+)/(?P<page>\d+)$',    'read'),
    url(r'^quiz/(?P<story>\d+)/(?P<section>\d+)$',                  'quiz'),
)

