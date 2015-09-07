from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib import admin
admin.autodiscover()

class HomePageView(TemplateView):
    template_name="index.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['apps'] = [
            { 
                'url' : 'wordquiz',
                'name' : 'Word Quiz',     
                'img' : 'wordquiz.png', 
                'desc' : 'Learn the meaning and sound of words through a quiz' 
            },
            { 
                'url' : 'choosepic',
                'name' : 'Pick the pic',  
                'img' : 'choosepic.png', 
                'desc' : 'Choose the picture that matches a given word' 
            },
            { 
                'url' : 'treasure',
                'name' : 'Treasure Hunt', 
                'img' : 'treasure.png', 
                'desc' : 'Follow the picture trail using the given clues' 
            },
        ]

        return context

urlpatterns = patterns('',
    url(r'^robots\.txt$', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    url(r'^$', HomePageView.as_view()),
    url(r'^about', TemplateView.as_view(template_name='about.html')),
    url(r'^contact', TemplateView.as_view(template_name='contact.html')),
    url(r'^wordquiz/', include('wordquiz.urls')),
    url(r'^choosepic/', include('choosepic.urls')),
    url(r'^treasure/', include('treasure.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
