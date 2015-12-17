from django.shortcuts import render_to_response
from alphabet.models import Lesson
from collections import defaultdict
from itertools import chain
import random

def get_lessons():
    d = defaultdict(list)
    for o in Lesson.objects.all():
        d[o.number].append(o.letter)
    # Getting rid of the default_factory allows us to use it
    # in a template. Otherwise we have to copy it to a dict
    x = { i[0]:i[1] for i in d.items()}
    return sorted(x.iteritems())

def index(request):
    lessons = get_lessons()
    print lessons
    context = {'lessons' : lessons}
    return render_to_response('alphabet/index.html', context)

def lesson(request, id=0):
    obj = Lesson.objects.filter(number = int(id))
    context = {'lesson' : id, 'letters' : obj}
    return render_to_response('alphabet/lesson.html', context)

def review(request, id=0):
    obj = Lesson.objects.filter(number = int(id))
    # Get a random letter from the past and append it to
    # the list that we're going to review
    past = Lesson.objects.filter(number__lt = int(id))
    past_len = len(past)
    if past_len:
        pastobj = past[random.randint(0, len(past)-1)]
        lesson = list(chain(obj, [pastobj]))
    else:
        lesson = obj

    context = {'lesson' : lesson}
    return render_to_response('alphabet/review.html', context)
