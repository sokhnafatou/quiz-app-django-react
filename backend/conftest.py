"""Fixtures partagées pour les tests pytest-django."""

import pytest
from django.core.management import call_command


@pytest.fixture
def sample_data(db):
    """Charge les quiz d'exemple via la commande de gestion."""
    call_command("load_sample_data")
