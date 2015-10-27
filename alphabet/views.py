from django.shortcuts import render_to_response
from alphabet.models import Lesson
from collections import defaultdict

def get_lessons():
    d = defaultdict(list)
    for o in Lesson.objects.all():
        d[o.number].append(o.letter)
    # Getting rid of the default_factory allows us to use it
    # in a template. Otherwise we have to copy it to a dict
    x = { str(i[0]):i[1] for i in d.items()}
    return sorted(x.iteritems())

def index(request):
    context = {'lessons' : get_lessons()}
    return render_to_response('alphabet/index.html', context)

def lesson(request, id=0):
    obj = Lesson.objects.filter(number = int(id))
    context = {'lesson' : id, 'letters' : obj}
    return render_to_response('alphabet/lesson.html', context)

def review(request, id=0):
    obj = Lesson.objects.filter(number = int(id))
    context = {'lesson' : obj}
    return render_to_response('alphabet/review.html', context)
