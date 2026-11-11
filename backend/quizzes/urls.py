"""Routes de l'API des quiz."""

from django.urls import path

from .views import (
    MySubmissionsView,
    QuizDetailView,
    QuizListView,
    SubmitQuizView,
)

urlpatterns = [
    path("", QuizListView.as_view(), name="quiz-list"),
    path("submissions/", MySubmissionsView.as_view(), name="my-submissions"),
    path("<int:pk>/", QuizDetailView.as_view(), name="quiz-detail"),
    path("<int:pk>/submit/", SubmitQuizView.as_view(), name="quiz-submit"),
]
