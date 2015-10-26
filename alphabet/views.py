from django.shortcuts import render_to_response

letters = [u'\u0d85', u'\u0da7']

def index(request):
    context = {'lessons' : ['a t', 'g m']}
    return render_to_response('alphabet/index.html', context)

def lesson(request, id=0):
    context = {'letters' : letters}
    return render_to_response('alphabet/lesson.html', context)

def review(request, id=0):
    context = {'letters' : letters}
    return render_to_response('alphabet/review.html', context)
