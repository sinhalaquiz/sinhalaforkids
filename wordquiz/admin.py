from wordquiz.models import WordCategory
from wordquiz.models import MediaObject
from wordquiz.models import SinhalaWord
from django.contrib import admin

admin.site.register(WordCategory)

class SinhalaWordAdmin(admin.ModelAdmin):
    list_display = ('word', 'category', 'english')

admin.site.register(SinhalaWord, SinhalaWordAdmin)

class MediaObjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'media_type')

admin.site.register(MediaObject, MediaObjectAdmin)
