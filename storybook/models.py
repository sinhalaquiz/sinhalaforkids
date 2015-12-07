from django.db import models

class Story(models.Model):
    # Story must have at least one page. When serving,
    # Four pages are generated consecutively.
    title = models.CharField(max_length=200)
    cover_image = models.URLField()
    level = models.IntegerField(default=0)

class Page(models.Model):
    # Each page must have at least one question. During
    # rendering, a question is chosen at random
    story = models.ForeignKey(Story)
    text = models.CharField(max_length=200)
    image = models.URLField()

class Question(models.Model):
    page = models.ForeignKey(Page)
    text = models.CharField(max_length=200)
    answer = models.CharField(max_length=32)
    incorrect1 = models.CharField(max_length=32)
    incorrect2 = models.CharField(max_length=32)

