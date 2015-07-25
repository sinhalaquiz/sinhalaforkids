from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^wordquiz/', include('wordquiz.urls')),
    url(r'^choosepic/', include('choosepic.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
