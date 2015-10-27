from django.contrib import admin
from alphabet.models import Lesson

admin.site.register(Lesson)

class LessonAdmin(admin.ModelAdmin):
    list_display = ('number', 'letter')


