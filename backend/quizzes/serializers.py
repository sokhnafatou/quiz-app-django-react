"""Serializers des quiz, questions et soumissions."""

from rest_framework import serializers

from .models import Choice, Question, Quiz, Submission


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ("id", "text", "is_correct")


class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ("id", "text", "order", "choices")


class QuizListSerializer(serializers.ModelSerializer):
    """Version allégée pour la liste des quiz (sans les questions)."""

    questions_count = serializers.IntegerField(source="questions.count", read_only=True)

    class Meta:
        model = Quiz
        fields = ("id", "title", "description", "questions_count", "created_at")


class QuizDetailSerializer(serializers.ModelSerializer):
    """Version détaillée avec toutes les questions et choix."""

    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = ("id", "title", "description", "questions", "created_at")


class SubmitQuizSerializer(serializers.Serializer):
    """
    Payload de soumission : liste de paires {question_id, choice_id}.
    Le score est calculé côté serveur à partir des choix marqués corrects.
    """

    answers = serializers.ListField(
        child=serializers.DictField(),
        allow_empty=False,
    )

    def validate_answers(self, value):
        cleaned = []
        for item in value:
            try:
                question_id = int(item["question_id"])
                choice_id = int(item["choice_id"])
            except (KeyError, TypeError, ValueError):
                raise serializers.ValidationError(
                    "Chaque réponse doit contenir 'question_id' et 'choice_id' (entiers)."
                )
            cleaned.append({"question_id": question_id, "choice_id": choice_id})
        return cleaned

    def save(self, **kwargs):
        quiz = kwargs["quiz"]
        user = kwargs["user"]
        answers = self.validated_data["answers"]

        submission = Submission.objects.create(user=user, quiz=quiz, score=0)

        score = 0
        for answer in answers:
            question = Question.objects.filter(id=answer["question_id"], quiz=quiz).first()
            if not question:
                continue
            choice = Choice.objects.filter(id=answer["choice_id"], question=question).first()
            if not choice:
                continue
            if choice.is_correct:
                score += 1
            from .models import Answer

            Answer.objects.create(
                submission=submission,
                question=question,
                choice=choice,
            )

        submission.score = score
        submission.save()
        return submission


class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ("id", "quiz", "score", "submitted_at")
