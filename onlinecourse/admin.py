from django.contrib import admin
from .models import (
    Course,
    Lesson,
    Instructor,
    Learner,
    Question,
    Choice,
    Submission,
)


class ChoiceInline(admin.TabularInline):
    """
    Inline admin representation of Choice objects within Question admin.
    """
    model = Choice
    extra = 5


class QuestionInline(admin.StackedInline):
    """
    Inline admin representation of Question objects within Lesson admin.
    """
    model = Question
    extra = 5


class QuestionAdmin(admin.ModelAdmin):
    """
    Admin configuration for Question model with ChoiceInline.
    """
    inlines = [ChoiceInline]
    list_display = ['question_text', 'grade']
    search_fields = ['question_text']


class LessonAdmin(admin.ModelAdmin):
    """
    Admin configuration for Lesson model with QuestionInline.
    """
    inlines = [QuestionInline]
    list_display = ['title', 'course']
    search_fields = ['title']


# Register seven models in Django Admin site
admin.site.register(Course)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Instructor)
admin.site.register(Learner)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Submission)
