"""
Modèles de l'application quizzes.

Un quiz contient plusieurs questions. Chaque question propose plusieurs
choix, dont un seul est considéré comme correct (pour cette démo).
Une soumission représente la tentative d'un utilisateur sur un quiz, et
contient les réponses choisies question par question.
"""

from django.conf import settings
from django.db import models


class Quiz(models.Model):
    title = models.CharField(max_length=200, verbose_name="Titre")
    description = models.TextField(blank=True, verbose_name="Description")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Quiz"
        verbose_name_plural = "Quiz"

    def __str__(self):
        return self.title


class Question(models.Model):
    quiz = models.ForeignKey(
        Quiz, related_name="questions", on_delete=models.CASCADE, verbose_name="Quiz"
    )
    text = models.CharField(max_length=500, verbose_name="Énoncé")
    order = models.PositiveIntegerField(default=0, verbose_name="Ordre")

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Question"

    def __str__(self):
        return f"{self.quiz.title} — {self.text[:50]}"


class Choice(models.Model):
    question = models.ForeignKey(
        Question, related_name="choices", on_delete=models.CASCADE, verbose_name="Question"
    )
    text = models.CharField(max_length=300, verbose_name="Texte")
    is_correct = models.BooleanField(default=False, verbose_name="Correct ?")

    class Meta:
        ordering = ["id"]
        verbose_name = "Choix"

    def __str__(self):
        return self.text


class Submission(models.Model):
    """Tentative d'un utilisateur sur un quiz, avec son score final."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="submissions",
        on_delete=models.CASCADE,
        verbose_name="Utilisateur",
    )
    quiz = models.ForeignKey(
        Quiz, related_name="submissions", on_delete=models.CASCADE, verbose_name="Quiz"
    )
    score = models.PositiveIntegerField(default=0, verbose_name="Score")
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-submitted_at"]
        verbose_name = "Soumission"

    def __str__(self):
        return f"{self.user.username} — {self.quiz.title} — {self.score}"


class Answer(models.Model):
    """Réponse choisie par l'utilisateur pour une question donnée."""

    submission = models.ForeignKey(
        Submission, related_name="answers", on_delete=models.CASCADE, verbose_name="Soumission"
    )
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, verbose_name="Question"
    )
    choice = models.ForeignKey(
        Choice, on_delete=models.CASCADE, verbose_name="Choix"
    )

    class Meta:
        verbose_name = "Réponse"

    def __str__(self):
        return f"{self.submission} — {self.question} — {self.choice}"
