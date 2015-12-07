from django.shortcuts import render_to_response

# Create your views here.
def index(request):
    context = {}
    return render_to_response('storybook/index.html', context)

def title(request, id=0):
    context = { 'title' : 'Story Title' }
    return render_to_response('storybook/title.html', context)

def read(request, id=0):
    context = {
            'title' : 'Story Title',
            'art'   : '/static/storybook/img/drawing.png',
            'text'  : 'Story text'
            }
    return render_to_response('storybook/read.html', context)

def quiz(request, id=0):
    context = {}
    return render_to_response('storybook/quiz.html', context)

def review(request, id=0):
    context = {}
    return render_to_response('storybook/review.html', context)
