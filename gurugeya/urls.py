from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^wordquiz/$', 'wordquiz.views.index'),
    url(r'^wordquiz/(?P<category>.+)/0$', 'wordquiz.views.firstQuestion'),
    url(r'^wordquiz/(?P<category>.*)/(?P<idx>[1-9][0-9]*)', 'wordquiz.views.nextQuestion'),
    url(r'^admin/', include(admin.site.urls)),
)
