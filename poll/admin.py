from django.contrib import admin
from .models import Question, Choice, Vote, Topic, Comment


# admin.site.register(Question)
# admin.site.register(Choice)

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2


class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]


admin.site.register(Topic)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Vote)
admin.site.register(Comment)