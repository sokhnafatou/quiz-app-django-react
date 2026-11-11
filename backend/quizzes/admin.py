"""Enregistrement des modèles de quiz dans le back-office Django."""

from django.contrib import admin

from .models import Choice, Question, Quiz, Submission


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at")
    search_fields = ("title",)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("quiz", "order", "text")
    list_filter = ("quiz",)


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ("question", "text", "is_correct")
    list_filter = ("question__quiz",)


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("user", "quiz", "score", "submitted_at")
    list_filter = ("quiz",)
