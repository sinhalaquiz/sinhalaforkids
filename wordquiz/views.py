from wordquiz.models import WordCategory
from wordquiz.models import SinhalaWord
from django.shortcuts import render_to_response
from django.http import HttpResponse

def index(request):
    categories = [cat for cat in WordCategory.objects.all()]
    used = [word.category for word in SinhalaWord.objects.all()]

    choices = [{'name' : cat.category, 'icon' : cat.img} 
            for cat in categories if cat in used]
    return render_to_response('wordquiz/index.html', { 'choices' : choices})

def firstQuestion(request, category):
    return HttpResponse("first question in category %s." % category)

def nextQuestion(request, category, idx):
    return HttpResponse("question %d in category %s." % (idx, category))

