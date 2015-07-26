from django.conf.urls import patterns, include, url

urlpatterns = patterns('choosepic.views',
    url(r'^$', 'index'),
    url(r'^(?P<category>.+)$', 'startGame'),
)

