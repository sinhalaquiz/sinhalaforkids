from django.conf.urls import patterns, include, url

urlpatterns = patterns('alphabet.views',
    url(r'^$', 'index'),
)

