from django.shortcuts import render
from wordquiz.models import SinhalaWord
from django.shortcuts import render_to_response
from django.template import RequestContext

def startGame(request, category):
    # First get all the words for a given category
    all_words = [i for i in SinhalaWord.objects.all() if str(i.category) == category]
    # Now construct a list of all the images from the words
    words = []
    urls = []
    for word in all_words:
        for m in word.media.all():
            if m.media_type == u'img':
                words.append(word)
                urls.append(m.url)

    print urls
    context = { 
            'words' : words[0:10], 
            'urls': urls[0:10]
    }
    return render_to_response('choosepic/game.html', context,
            context_instance=RequestContext(request))

def index(request):
    return startGame(request, 'animals')

