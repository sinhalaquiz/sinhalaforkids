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

class AlphabetPageView(TemplateView):
    template_name="app.html"

    def get_context_data(self, **kwargs):
        context = super(AlphabetPageView, self).get_context_data(**kwargs)
        context['title'] = 'Sinhala alphabet'
        context['desc'] = 'Learn the recognise the shapes and sounds of the ' \
            'Sinhala alphabet'
        context['heading'] = 'Choose your lesson'
        context['url'] = '/app/alphabet'

        return context

class WordsPageView(TemplateView):
    template_name="index.html"

    def get_context_data(self, **kwargs):
        context = super(WordsPageView, self).get_context_data(**kwargs)
        context['title'] = 'Learn Sinhala words'
        context['desc'] = 'Expand your vocabulary through these activities'
        context['heading'] = 'Choose your activity'
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
        ]

        return context

class SentencesPageView(TemplateView):
    template_name="index.html"

    def get_context_data(self, **kwargs):
        context = super(SentencesPageView, self).get_context_data(**kwargs)
        context['title'] = 'Learning Sentences'
        context['desc'] = 'Activities to help learn to read and understand sentences in Sinhala'
        context['heading'] = 'Choose your activity'
        context['apps'] = [
            { 
                'url' : 'treasure',
                'name' : 'Treasure Hunt', 
                'img' : 'treasure.png', 
                'desc' : 'Follow the picture trail using the given clues' 
                },
            {
                'url' : 'storybook',
                'name' : 'Story Book', 
                'img' : 'treasure.png', 
                'desc' : 'Read a story from a selection of e-books'
                },
            ]

        return context

class ChoosepicAppView(TemplateView):
    template_name="app.html"

    def get_context_data(self, **kwargs):
        context = super(ChoosepicAppView, self).get_context_data(**kwargs)
        context['title'] = 'Choose the picture'
        context['desc'] = 'Choose the picture that matches the given word'
        context['heading'] = 'Choose the picture'
        context['url'] = '/app/choosepic'

        return context

class WordQuizAppView(TemplateView):
    template_name="app.html"

    def get_context_data(self, **kwargs):
        context = super(WordQuizAppView, self).get_context_data(**kwargs)
        context['title'] = 'Word Quiz'
        context['desc'] = 'Learn the meaning and sound of words through a quiz' 
        context['heading'] = 'Identify the word'
        context['url'] = '/app/wordquiz'

        return context

class StoryBookAppView(TemplateView):
    template_name="app.html"

    def get_context_data(self, **kwargs):
        context = super(StoryBookAppView, self).get_context_data(**kwargs)
        context['title'] = 'Story Book'
        context['desc'] = 'Read a story from a selection of e-books'
        context['heading'] = 'Select a book'
        context['url'] = '/app/storybook'

        return context

urlpatterns = patterns('',
        url(r'^robots\.txt$', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
        url(r'^$', HomePageView.as_view()),
        url(r'^alphabet', AlphabetPageView.as_view()),
        url(r'^choosepic', ChoosepicAppView.as_view()),
        url(r'^wordquiz', WordQuizAppView.as_view()),
        url(r'^storybook', StoryBookAppView.as_view()),
        url(r'^words', WordsPageView.as_view()),
        url(r'^sentences', SentencesPageView.as_view()),
        url(r'^about', TemplateView.as_view(template_name='about.html')),
        url(r'^contact', TemplateView.as_view(template_name='contact.html')),
        url(r'^app/wordquiz/', include('wordquiz.urls')),
        url(r'^app/choosepic/', include('choosepic.urls')),
        url(r'^treasure/', include('treasure.urls')),
        url(r'^app/storybook/', include('storybook.urls')),
        url(r'^app/alphabet/', include('alphabet.urls')),
        url(r'^admin/', include(admin.site.urls)),
        )
