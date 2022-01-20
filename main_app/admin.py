from django.contrib import admin

from main_app.models import Choice, Question, Quiz


class InlineChoice(admin.TabularInline):
    model = Choice


class QuestionAdmin(admin.ModelAdmin):
    inlines = [InlineChoice]


admin.site.register(Question, QuestionAdmin)
admin.site.register(Quiz)
