from django.db import models

# Each word the student learns belongs to a specific category
# such as animals,actions,anatomy, etc. This model represents
# that.
class WordCategory(models.Model):
    def __unicode__(self):
        return self.category

    category = models.CharField(max_length=64)
    img = models.URLField()

# A media object is a non-textual representation of a word.
# It can be an image, video or an audio clip. Sometimes the
# media object can be ambiguous (e.g. an image might have a
# mouth where the expected match is 'chin'. These are in a
# list of exclusions
class MediaObject(models.Model):
    def __unicode__(self):
        return self.title

    MEDIA_TYPE_OPTIONS = (
        (u'vid', u'Video'),
        (u'aud', u'Audio'),
        (u'img', u'Image')
    )
    url = models.URLField()
    media_type = models.CharField(max_length=3, choices=MEDIA_TYPE_OPTIONS)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200, blank=True)
    source = models.URLField(blank=True)
    exclusions = models.ManyToManyField('SinhalaWord', blank=True)

# A Sinhala word is what we test for in our exercises. It
# has an English word that we use as a translation source. It
# also can be represented by media objects
class SinhalaWord(models.Model):
    def __unicode__(self):
        return self.word
    word = models.CharField(max_length=32, unique=True)
    category = models.ForeignKey("WordCategory")
    english = models.CharField(max_length=32)
    media = models.ManyToManyField('MediaObject', blank=True)

