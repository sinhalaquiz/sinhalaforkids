from django.conf.urls import patterns, include, url

urlpatterns = patterns('wordquiz.views',
    url(r'^$', 'index'),
    url(r'^(?P<category>.+)/0$', 'firstQuestion'),
    url(r'^(?P<category>.*)/(?P<idx>[1-9][0-9]*)', 'nextQuestion'),
)

