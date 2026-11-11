"""Tests de l'API des quiz (liste, détail, soumission, historique)."""

import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from quizzes.models import Choice, Question, Quiz


@pytest.fixture
def user():
    return User.objects.create_user(username="eve", password="Str0ngPassw0rd!")


@pytest.fixture
def auth_client(user):
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def public_client():
    return APIClient()


def _build_quiz():
    quiz = Quiz.objects.create(title="Quiz test", description="Pour les tests")
    q1 = Question.objects.create(quiz=quiz, text="1 + 1 ?", order=0)
    Choice.objects.create(question=q1, text="1", is_correct=False)
    Choice.objects.create(question=q1, text="2", is_correct=True)
    q2 = Question.objects.create(quiz=quiz, text="Couleur du ciel le jour ?", order=1)
    Choice.objects.create(question=q2, text="Bleu", is_correct=True)
    Choice.objects.create(question=q2, text="Vert", is_correct=False)
    return quiz


@pytest.mark.django_db
def test_list_quizzes_is_public(sample_data, public_client):
    response = public_client.get("/api/quizzes/")
    assert response.status_code == 200
    assert len(response.data) == 2
    titles = {item["title"] for item in response.data}
    assert "Capitales d'Afrique" in titles
    assert "Bases de Python" in titles


@pytest.mark.django_db
def test_list_quiz_includes_questions_count(sample_data, public_client):
    response = public_client.get("/api/quizzes/")
    item = next(i for i in response.data if i["title"] == "Bases de Python")
    assert item["questions_count"] == 5


@pytest.mark.django_db
def test_quiz_detail_returns_questions_and_choices(sample_data, public_client):
    quizzes = public_client.get("/api/quizzes/").json()
    quiz_id = next(i["id"] for i in quizzes if i["title"] == "Capitales d'Afrique")
    response = public_client.get(f"/api/quizzes/{quiz_id}/")
    assert response.status_code == 200
    assert len(response.data["questions"]) == 5
    first_question = response.data["questions"][0]
    assert len(first_question["choices"]) == 4


@pytest.mark.django_db
def test_submit_requires_authentication(public_client):
    quiz = _build_quiz()
    response = public_client.post(
        f"/api/quizzes/{quiz.id}/submit/",
        {"answers": []},
        format="json",
    )
    assert response.status_code == 401


@pytest.mark.django_db
def test_submit_calculates_score(auth_client):
    quiz = _build_quiz()
    q1, q2 = quiz.questions.order_by("order")
    correct_q1 = q1.choices.get(is_correct=True).id
    correct_q2 = q2.choices.get(is_correct=True).id
    response = auth_client.post(
        f"/api/quizzes/{quiz.id}/submit/",
        {
            "answers": [
                {"question_id": q1.id, "choice_id": correct_q1},
                {"question_id": q2.id, "choice_id": correct_q2},
            ]
        },
        format="json",
    )
    assert response.status_code == 201
    assert response.data["score"] == 2


@pytest.mark.django_db
def test_submit_partial_score(auth_client):
    quiz = _build_quiz()
    q1, q2 = quiz.questions.order_by("order")
    correct_q1 = q1.choices.get(is_correct=True).id
    wrong_q2 = q2.choices.get(is_correct=False).id
    response = auth_client.post(
        f"/api/quizzes/{quiz.id}/submit/",
        {
            "answers": [
                {"question_id": q1.id, "choice_id": correct_q1},
                {"question_id": q2.id, "choice_id": wrong_q2},
            ]
        },
        format="json",
    )
    assert response.status_code == 201
    assert response.data["score"] == 1


@pytest.mark.django_db
def test_submit_rejects_invalid_payload(auth_client):
    quiz = _build_quiz()
    response = auth_client.post(
        f"/api/quizzes/{quiz.id}/submit/",
        {"answers": [{"question_id": "x"}]},
        format="json",
    )
    assert response.status_code == 400


@pytest.mark.django_db
def test_my_submissions_history(auth_client):
    quiz = _build_quiz()
    q1, q2 = quiz.questions.order_by("order")
    correct_q1 = q1.choices.get(is_correct=True).id
    correct_q2 = q2.choices.get(is_correct=True).id
    auth_client.post(
        f"/api/quizzes/{quiz.id}/submit/",
        {
            "answers": [
                {"question_id": q1.id, "choice_id": correct_q1},
                {"question_id": q2.id, "choice_id": correct_q2},
            ]
        },
        format="json",
    )
    response = auth_client.get("/api/quizzes/submissions/")
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["score"] == 2


@pytest.mark.django_db
def test_my_submissions_requires_authentication(public_client):
    response = public_client.get("/api/quizzes/submissions/")
    assert response.status_code == 401


@pytest.mark.django_db
def test_load_sample_data_is_idempotent(db):
    from django.core.management import call_command

    call_command("load_sample_data")
    call_command("load_sample_data")
    assert Quiz.objects.filter(title="Bases de Python").count() == 1
    assert Question.objects.filter(quiz__title="Bases de Python").count() == 5
