from django.conf.urls import patterns, include, url

urlpatterns = patterns('treasure.views',
    url(r'^$', 'index'),
)

