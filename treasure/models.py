from django.db import models
from wordquiz.models import MediaObject

class Clue(models.Model):
    def __unicode__(self):
        return self.clue

    clue = models.CharField(max_length=200)
    img = models.ForeignKey(MediaObject)

