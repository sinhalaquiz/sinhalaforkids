from django.shortcuts import render_to_response
from storybook.models import Story
from storybook.models import Section
from storybook.models import Page
import random

# The view interface functions
def index(request):
    stories = Story.objects.all()
    context = {
            'stories' : stories
            }
    return render_to_response('storybook/index.html', context)

def title(request, story):
    obj = Story.objects.get(id = story)
    context = { 
            'title'   : obj.title,
            'art'     : obj.cover_image,
            'story'   : story,
            'section' : 0,
            'page'    : 0
            }
    return render_to_response('storybook/title.html', context)

def read(request, story, section, page):
    # Get the list of pages in the story
    obj = Story.objects.get(id = story)
    section_obj = obj.section_set.all()[int(section)]
    pages = list(section_obj.page_set.all())
    page = int(page)
    next_page = page + 1
    page_obj = pages[page]
    if next_page < len(pages):
        context = {
                'title' : obj.title,
                'art'   : page_obj.image,
                'text'  : page_obj.text,
                'story'     : story,
                'section'   : section,
                'page'  : next_page
                }
        return render_to_response('storybook/read-section-mid.html', context)

    context = {
            'title'     : obj.title,
            'art'       : page_obj.image,
            'text'      : page_obj.text,
            'story'     : story,
            'section'   : section
            }
    return render_to_response('storybook/read-section-end.html', context)

def shuffle(x):
    random.shuffle(x)
    return x

def quiz(request, story, section):
    obj = Story.objects.get(id = story)
    section_obj = obj.section_set.all()[int(section)]
    next_section = int(section) + 1
    questions = [ {
            'text' : q.text,
            'ans'  : q.answer,
            'choices' : shuffle([q.answer, q.incorrect1, q.incorrect2])
        } for q in section_obj.question_set.all()]
    if next_section < obj.section_set.count():
        context = {
                'title'     : obj.title,
                'questions' : questions,
                'story'     : story,
                'section'   : next_section,
                'page'      : 0
        }
        return render_to_response('storybook/quiz-story-mid.html', context)
    context = {
            'questions' : questions,
            'story'     : story,
    }
    return render_to_response('storybook/quiz-story-end.html', context)

