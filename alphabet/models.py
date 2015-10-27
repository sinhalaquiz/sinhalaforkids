from django.db import models

class Lesson(models.Model):
    def __unicode__(self):
        return self.letter

    number = models.IntegerField()
    letter = models.CharField(max_length=16)
    audio = models.URLField()

