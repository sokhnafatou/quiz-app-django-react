"""Tests de l'API d'authentification (inscription / connexion / profil)."""

import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient


@pytest.fixture
def client():
    return APIClient()


@pytest.mark.django_db
def test_register_creates_user(client):
    payload = {
        "username": "alice",
        "email": "alice@example.com",
        "password": "Str0ngPassw0rd!",
    }
    response = client.post("/api/auth/register/", payload, format="json")
    assert response.status_code == 201
    assert response.data["username"] == "alice"
    assert "password" not in response.data
    assert User.objects.filter(username="alice").count() == 1


@pytest.mark.django_db
def test_register_rejects_duplicate_username(client):
    User.objects.create_user(username="bob", password="Str0ngPassw0rd!")
    payload = {"username": "bob", "email": "bob@example.com", "password": "Str0ngPassw0rd!"}
    response = client.post("/api/auth/register/", payload, format="json")
    assert response.status_code == 400


@pytest.mark.django_db
def test_login_returns_jwt_tokens(client):
    User.objects.create_user(username="carol", password="Str0ngPassw0rd!")
    response = client.post(
        "/api/auth/login/",
        {"username": "carol", "password": "Str0ngPassw0rd!"},
        format="json",
    )
    assert response.status_code == 200
    assert "access" in response.data
    assert "refresh" in response.data


@pytest.mark.django_db
def test_login_rejects_bad_credentials(client):
    User.objects.create_user(username="carol", password="Str0ngPassw0rd!")
    response = client.post(
        "/api/auth/login/",
        {"username": "carol", "password": "wrong"},
        format="json",
    )
    assert response.status_code == 401


@pytest.mark.django_db
def test_me_requires_authentication(client):
    response = client.get("/api/auth/me/")
    assert response.status_code == 401


@pytest.mark.django_db
def test_me_returns_authenticated_user(client):
    user = User.objects.create_user(username="dave", password="Str0ngPassw0rd!")
    client.force_authenticate(user=user)
    response = client.get("/api/auth/me/")
    assert response.status_code == 200
    assert response.data["username"] == "dave"
