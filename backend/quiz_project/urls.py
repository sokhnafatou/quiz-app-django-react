"""
URL configuration for quiz_project project.

Routes racine de l'API :
- /api/auth/     : inscription et connexion (JWT)
- /api/quizzes/  : liste, détail et soumission des quiz
- /admin/        : back-office Django
"""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("accounts.urls")),
    path("api/quizzes/", include("quizzes.urls")),
]
