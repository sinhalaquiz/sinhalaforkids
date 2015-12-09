from django.shortcuts import render_to_response
from storybook.models import Story
from storybook.models import Section
from storybook.models import Page

# The view interface functions
def index(request):
    stories = Story.objects.all()
    context = {
            'stories' : stories
            }
    return render_to_response('storybook/index.html', context)

def title(request, story):
    obj = Story.objects.get(id = story)
    section = obj.section_set.all()[0]
    first_page = section.page_set.all()[0]
    context = { 
            'title'   : obj.title,
            'art'     : obj.cover_image,
            'story'   : story,
            'section' : section.pk,
            'page'    : 0
            }
    return render_to_response('storybook/title.html', context)

def read(request, story, section, page):
    # Get the list of pages in the story
    obj = Story.objects.get(id = story)
    section_obj = Section.objects.get(pk=section)
    pages = [i for i in section_obj.page_set.all()]
    page = int(page)
    next_page = page + 1
    page_obj = pages[page]
    if next_page < len(pages):
        context = {
                'title' : obj.title,
                'art'   : page_obj.image,
                'text'  : page_obj.text,
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

def quiz(request, story, section):
    context = {}
    return render_to_response('storybook/quiz.html', context)

def review(request, id=0):
    context = {}
    return render_to_response('storybook/review.html', context)
