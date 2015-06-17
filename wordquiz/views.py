from wordquiz.models import WordCategory
from wordquiz.models import SinhalaWord
from django.shortcuts import render_to_response

def index(request):
    categories = [cat for cat in WordCategory.objects.all()]
    used = [word.category for word in SinhalaWord.objects.all()]

    choices = [{'name' : cat.category, 'icon' : cat.img} 
            for cat in categories if cat in used]
    return render_to_response('wordquiz/index.html', { 'choices' : choices})
