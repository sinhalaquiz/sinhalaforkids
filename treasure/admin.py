from treasure.models import Clue
from django.contrib import admin

class ClueAdmin(admin.ModelAdmin):
    list_display = ('clue', 'img')

admin.site.register(Clue, ClueAdmin)

