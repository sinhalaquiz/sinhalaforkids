from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib import admin
admin.autodiscover()

class HomePageView(TemplateView):
    template_name="index.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['apps'] = ['choosepic', 'wordquiz']
        return context

urlpatterns = patterns('',
        url(r'^$', HomePageView.as_view()),
        url(r'^wordquiz/', include('wordquiz.urls')),
        url(r'^choosepic/', include('choosepic.urls')),
        url(r'^treasure/', include('treasure.urls')),
        url(r'^admin/', include(admin.site.urls)),
        )
