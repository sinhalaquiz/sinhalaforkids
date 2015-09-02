import random
from django.shortcuts import render_to_response
from treasure.models import Clue

def getImgUrl(img):
    return img.url

def getClues():
    # Retrieve all the clues from the model
    clues = [{'src' : getImgUrl(clue.img), 'clue' : clue.clue} for clue in Clue.objects.all()]
    random.shuffle(clues)
    # Return the top six
    return clues[0:6]

def index(request):
    context = {'clues' : getClues()}
    return render_to_response('treasure/game.html', context)
