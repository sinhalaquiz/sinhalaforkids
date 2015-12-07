from django.conf.urls import patterns, include, url

urlpatterns = patterns('storybook.views',
    url(r'^$',          'index'),
    url(r'^index$',     'index'),
    url(r'^title$',     'title'),
    url(r'^read$',      'read'),
    url(r'^quiz$',      'quiz'),
    url(r'^review$',    'review'),
)

