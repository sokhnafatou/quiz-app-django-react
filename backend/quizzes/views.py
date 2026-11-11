"""Vues de l'API des quiz."""

from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Quiz, Submission
from .serializers import (
    QuizDetailSerializer,
    QuizListSerializer,
    SubmitQuizSerializer,
    SubmissionSerializer,
)


class QuizListView(generics.ListAPIView):
    """GET /api/quizzes/ : liste tous les quiz (public)."""

    queryset = Quiz.objects.all()
    serializer_class = QuizListSerializer
    permission_classes = [permissions.AllowAny]


class QuizDetailView(generics.RetrieveAPIView):
    """GET /api/quizzes/<id>/ : détail d'un quiz avec ses questions (public)."""

    queryset = Quiz.objects.all()
    serializer_class = QuizDetailSerializer
    permission_classes = [permissions.AllowAny]


class SubmitQuizView(APIView):
    """POST /api/quizzes/<id>/submit/ : enregistre les réponses et calcule le score."""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        quiz = get_object_or_404(Quiz, pk=pk)
        serializer = SubmitQuizSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        submission = serializer.save(quiz=quiz, user=request.user)
        return Response(
            SubmissionSerializer(submission).data,
            status=status.HTTP_201_CREATED,
        )


class MySubmissionsView(generics.ListAPIView):
    """GET /api/quizzes/submissions/ : historique des tentatives de l'utilisateur."""

    serializer_class = SubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Submission.objects.filter(user=self.request.user)
