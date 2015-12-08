from django.contrib import admin
from storybook.models import Story
from storybook.models import Page
from storybook.models import Question
from storybook.models import Section

#admin.site.register(Question, QuestionAdmin)

class QuestionInline(admin.StackedInline):
    model = Question
    extra = 4

class PageInline(admin.StackedInline):
    model = Page
    extra = 2

class StoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'level')

admin.site.register(Story, StoryAdmin)

class SectionAdmin(admin.ModelAdmin):
    inlines = [PageInline, QuestionInline]

admin.site.register(Section, SectionAdmin)
