from django.db import models

class Story(models.Model):
    def __unicode__(self):
        return self.title
    title = models.CharField(max_length=200)
    cover_image = models.URLField()
    level = models.IntegerField(default=0)

class Section(models.Model):
    def __unicode__(self):
        return "%s - %d" % (self.story.title, self.pk)
    story = models.ForeignKey(Story)
    
class Page(models.Model):
    def __unicode__(self):
        return self.text
    section = models.ForeignKey(Section)
    text = models.CharField(max_length=200)
    image = models.URLField()

class Question(models.Model):
    def __unicode__(self):
        return self.text
    section = models.ForeignKey(Section)
    text = models.CharField(max_length=200)
    answer = models.CharField(max_length=32)
    incorrect1 = models.CharField(max_length=32)
    incorrect2 = models.CharField(max_length=32)

