import random
from wordquiz.models import WordCategory
from wordquiz.models import SinhalaWord
from wordquiz.models import MediaObject
from django.shortcuts import render_to_response, Http404
from django.template import RequestContext

def get_choices(category, answer, exclusions):
    all_words = [i.word for i in SinhalaWord.objects.all() if i.category == category]
    exclusions.append(answer)
    all_wrong = [w for w in all_words if w not in exclusions]
    random.shuffle(all_wrong)
    choices = all_wrong[0:3]
    choices.append(answer)
    random.shuffle(choices)
    return choices

def get_text_exercise_data(exercise):
    obj = SinhalaWord.objects.get(id = exercise['qid'])
    choices = get_choices(obj.category, obj.word, [])
    return { 
            'template' : 'identify-english.html', 
            'question' : obj.english,
            'answer' : obj.word,
            'choices' : choices 
    }

def build_youtube_embed_url(url):
    m = re.search(r'\?v=(.{11})', url)
    vid = m.group(1)
    if not vid:
        return url
    return 'http://www.youtube.com/embed/' + vid 

def build_url_nop(url):
    return url

def get_media_exercise_data(exercise):
    obj = SinhalaWord.objects.get(id = exercise['qid'])
    print exercise['objid']
    media = MediaObject.objects.get(id = exercise['objid'])

    # media_type is the index for build_info
    build_info = {
            'vid' : {'url_op' : build_youtube_embed_url, 'template' : 'identify-video.html'},
            'aud' : {'url_op' : build_url_nop,           'template' : 'identify-audio.html'},
            'img' : {'url_op' : build_url_nop,           'template' : 'identify-image.html'},
    }

    b = build_info[media.media_type]
    question = b['url_op'](media.url)
    exclusions = [ex.word for ex in media.exclusions.all()]
    choices = get_choices(obj.category, obj.word, exclusions)
    return { 
            'template' : b['template'],
            'question' : question,
            'answer' : obj.word,
            'choices' : choices 
    }

def get_exercise_data(exercise):
    if exercise['type'] == 'txt':
        return get_text_exercise_data(exercise)
    else:
        return get_media_exercise_data(exercise)

def get_all_exercises(category):
    # Choose all the words that belong to the selected category
    word_objects = [i for i in SinhalaWord.objects.all() if str(i.category) == category]
    exercises = []

    for w in word_objects:
        # First build the question specific data for the English translation
        exercises.append({'qid' : w.id, 'type' : 'txt', 'objid' : None})
        # Now build builders using the media objects
        for m in w.media.all():
            exercises.append({'qid' : w.id, 'type' : 'media', 'objid' : m.id})
    return exercises

def create_exercise_list(category):
    # Fetch all the questions
    exercises = get_all_exercises(category)
    # Pick the first 20 questions after shuffling them
    random.shuffle(exercises)
    l = exercises[0:20]
    return l

def present_next_question(request, category, exercises, idx, score):
    #try:
    ex = get_exercise_data(exercises[idx])
    #except:
    #    raise Http404

    payload = { 
        'cat' : category, 
        'question': ex['question'], 
        'answer' : ex['answer'],
        'choices' : ex['choices'], 
        'queue' : exercises, 
        'idx' : idx + 1,
        'score' : score
    }

    return render_to_response('wordquiz/' + ex['template'], payload,
            context_instance=RequestContext(request))

def is_correct_choice(choice, exercise):
    qid = exercise['qid']
    obj = SinhalaWord.objects.get(id = qid)
    return choice == obj.word

def display_score(score, total):
    context = { 
        'score' : score,
        'total' : total
    }
    return render_to_response('wordquiz/results.html', context)

def index(request):
    categories = [cat for cat in WordCategory.objects.all()]
    used = [word.category for word in SinhalaWord.objects.all()]

    choices = [{'name' : cat.category, 'icon' : cat.img} 
            for cat in categories if cat in used]
    return render_to_response('wordquiz/index.html', { 'choices' : choices})

def firstQuestion(request, category):
    exercises = create_exercise_list(category)
    return present_next_question(request, category, exercises, 0, 0)

def nextQuestion(request, category, idx):
    exercises = eval(request.POST['queue'])
    category = request.POST['cat']
    score = eval(request.POST['score'])
    choice = request.POST[u'choice']
    i = eval(idx)

    # The idx contains the next exercise so we need to get the
    # previous one for comparison
    if (is_correct_choice(choice, exercises[i-1])):
        score = score + 1

    if i < len(exercises):
        return present_next_question(request, category, exercises, i, score)
    return display_score(score, len(exercises))

