from django.shortcuts import render_to_response
from alphabet.models import Lesson

def index(request):
    context = {'lessons' : ['a t', 'g m']}
    return render_to_response('alphabet/index.html', context)

def lesson(request, id=0):
    obj = Lesson.objects.filter(number = int(id))
    context = {'lesson' : id, 'letters' : obj}
    return render_to_response('alphabet/lesson.html', context)

def review(request, id=0):
    obj = Lesson.objects.filter(number = int(id))
    context = {'lesson' : obj}
    return render_to_response('alphabet/review.html', context)
