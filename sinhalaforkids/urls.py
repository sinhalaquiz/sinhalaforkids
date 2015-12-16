from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib import admin
admin.autodiscover()

class HomePageView(TemplateView):
    template_name="index.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['title'] = 'Sinhala for kids'
        context['desc'] = 'Sinhala for kids is a site dedicated to children ' \
                'learning Sinhala as a second language. Its primary ' \
                'goal is to promote skills in reading and comprehension'
        context['heading'] = 'Choose your class'
        context['apps'] = [
            { 
                'url' : 'alphabet',
                'name' : 'Alphabet',     
                'img' : 'alphabet.png', 
                'desc' : 'Learn to recognise the shapes and sounds of the Sinhala alphabet' 
            },
            { 
                'url' : 'words',
                'name' : 'Learn words',  
                'img' : 'words.png', 
                'desc' : 'Build your vocabulary through games and quizes' 
            },
            { 
                'url' : 'sentences',
                'name' : 'Read sentences', 
                'img' : 'sentences.png', 
                'desc' : 'Learn to read and understand senteces' 
            },
        ]

        return context

class AppRepo():
    apps = [
        {
            'name'  : 'alphabet',
            'category' : 'alphabet',
            'title' :  'Sinhala alphabet',
            'img' : 'alphabet.png', 
            'desc' : 'Learn to recognise the shapes and sounds of the ' \
                     'Sinhala alphabet',
            'url' : 'alphabet',
        },
        {
            'name' : 'choosepic',
            'category' : 'words',
            'title' : 'Choose the picture',
            'img' : 'choosepic.png', 
            'desc' :  'Choose the picture that matches the given word',
            'url' :  'choosepic',
        },
        {
            'name' : 'wordquiz',
            'category' : 'words',
            'title' : 'Word Quiz',
            'img' : 'wordquiz.png', 
            'desc' : 'Learn the meaning and sound of words through a quiz',
            'url' : 'wordquiz',
        },
        { 
            'name' : 'Treasure Hunt', 
            'category' : 'sentences',
            'title' : 'Treasure Hunt',
            'img' : 'treasure.png', 
            'desc' : 'Follow the picture trail using the given clues',
            'url' : 'treasure',
        },
        {
            'name' : 'storybook', 
            'category' : 'sentences',
            'title' : 'Story Book',
            'img' : 'treasure.png', 
            'desc' : 'Read a story from a selection of e-books',
            'url' : 'storybook',
        },
     ]


class AppView(TemplateView, AppRepo):
    name = None
    template_name = "app.html"

    def _get_app_context(self, name, context):
        for a in self.apps:
            if a['name'] == name:
                context['title'] = a['title']
                context['desc'] = a['desc']
                context['url'] = a['url']
                break

        return context

    def get_context_data(self, **kwargs):
        context = super(TemplateView, self).get_context_data(**kwargs)
        return self._get_app_context(self.name, context)

class CategoryPageView(TemplateView, AppRepo):
    template_name = "index.html"
    category = None

    def get_context_data(self, **kwargs):
        context = super(CategoryPageView, self).get_context_data(**kwargs)

        cat_apps = []
        for a in self.apps:
            if a['category'] == self.category:
                cat_apps.append({
                    'url' : a['url'],
                    'name' : a['name'],
                    'img' : a['img'],
                    'desc' : a['desc']
                })

        context['title'] = 'Learn Sinhala words'
        context['desc'] = 'Expand your vocabulary through these activities'
        context['heading'] = 'Choose your activity'
        context['apps'] = cat_apps

        return context

urlpatterns = patterns('',
        url(r'^robots\.txt$', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
        url(r'^$', HomePageView.as_view()),
        url(r'^alphabet', AppView.as_view(name='alphabet')),
        url(r'^choosepic', AppView.as_view(name='choosepic')),
        url(r'^wordquiz', AppView.as_view(name='wordquiz')),
        url(r'^storybook', AppView.as_view(name='storybook')),
        url(r'^words', CategoryPageView.as_view(category='words')),
        url(r'^sentences', CategoryPageView.as_view(category='sentences')),
        url(r'^about', TemplateView.as_view(template_name='about.html')),
        url(r'^contact', TemplateView.as_view(template_name='contact.html')),
        url(r'^app/wordquiz/', include('wordquiz.urls')),
        url(r'^app/choosepic/', include('choosepic.urls')),
        url(r'^treasure/', include('treasure.urls')),
        url(r'^app/storybook/', include('storybook.urls')),
        url(r'^app/alphabet/', include('alphabet.urls')),
        url(r'^admin/', include(admin.site.urls)),
        )
