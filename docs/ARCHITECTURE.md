# Architecture

Ce document explique, simplement, les choix techniques de l'application QuizEdu.

## Vue d'ensemble

L'application est découpée en trois services indépendants qui communiquent
uniquement via HTTP/JSON :

1. **Frontend** (React + Vite) — interface utilisateur servie par nginx.
2. **Backend** (Django + Django REST Framework) — API REST authentifiée par JWT.
3. **Base de données** (PostgreSQL) — stockage persistant des utilisateurs,
   quiz, questions et scores.

```
┌──────────────┐     HTTP/JSON      ┌──────────────┐      SQL       ┌──────────────┐
│  Frontend    │  ───────────────> │   Backend    │  ──────────>  │  PostgreSQL  │
│  React/Vite  │  <─────────────── │  Django DRF  │  <──────────  │              │
│  (nginx)     │   REST + JWT      │  (gunicorn)  │               │              │
└──────────────┘                   └──────────────┘               └──────────────┘
```

## Pourquoi ces choix ?

### Backend : Django + Django REST Framework

- **Django** fournit un ORM, un système d'authentification et un back-office
  admin prêts à l'emploi, ce qui accélère le développement d'une API.
- **DRF** ajoute des serializers, des vues génériques et une négociation de
  contenu claire, idéale pour exposer une API REST propre.
- L'authentification repose sur **SimpleJWT** : le frontend reçoit un token
  d'accès (court) et un token de rafraîchissement (long), qu'il envoie dans
  l'en-tête `Authorization: Bearer <token>`.

### Frontend : React + Vite

- **React** permet de construire une interface par composants réutilisables
  (Navbar, pages, formulaires).
- **Vite** offre un démarrage à chaud très rapide et un build de production
  optimisé (assets minifiés et hashés).
- **React Router** gère la navigation côté client (accueil, quiz, historique,
  connexion, inscription).
- L'état d'authentification est partagé via un **Context React**
  (`AuthContext`), ce qui évite de propager le token manuellement dans toute
  l'arborescence de composants.

### Base de données : PostgreSQL

- **PostgreSQL** est une base relationnelle robuste et largement utilisée en
  production. Elle convient bien aux données structurées (quiz, questions,
  choix, utilisateurs, scores).
- En développement local sans Docker, le backend bascule automatiquement sur
  **SQLite** (si `POSTGRES_HOST` n'est pas défini), afin de pouvoir lancer
  les tests sans installer PostgreSQL.

### Conteneurisation : Docker

- Chaque service a son propre `Dockerfile`, ce qui garantit un
  environnement reproductible.
- **Docker Compose** orchestre les trois services avec une seule commande
  (`docker compose up --build`) et gère la dépendance entre le backend et la
  base de données (le backend attend que PostgreSQL soit sain avant de
  démarrer).
- Le frontend est servi par **nginx** en production, qui renvoie toutes les
  routes inconnues vers `index.html` (routing côté client).

## Modèle de données

```
User (Django) ──< Submission >── Quiz
                       │
                       └── Answer ── Question ── Choice
```

- Un **Quiz** contient plusieurs **Questions** (ordonnées).
- Chaque **Question** propose plusieurs **Choices**, dont un seul est marqué
  `is_correct`.
- Une **Submission** représente la tentative d'un utilisateur sur un quiz ;
  elle contient un **Score** (nombre de bonnes réponses) et plusieurs
  **Answers** (une par question répondue).
- Le score est **calculé côté serveur** à la soumission, jamais côté client,
  pour éviter toute triche possible.

## Sécurité

- Aucun secret n'est commité : la configuration passe par des variables
  d'environnement (voir `.env.example`).
- Les mots de passe sont hashés par Django (PBKDF2 par défaut).
- L'authentification API se fait par JWT ; les endpoints de soumission et
  d'historique exigent un token valide.
- Le frontend n'est jamais trusted : le score est recalculé serveur.

## Tests et CI

- Les tests backend utilisent **pytest** + **pytest-django** et couvrent
  l'authentification, les endpoints de quiz et le calcul du score.
- Le workflow GitHub Actions (`.github/workflows/ci.yml`) exécute les tests
  backend et le build frontend à chaque push et sur chaque pull request.

## Limites connues (projet de démo)

- Pas de rafraîchissement automatique du token JWT côté frontend (le token
  expire après 1 h).
- Pas de pagination sur la liste des quiz (volume faible en démo).
- Pas de limite de taux (rate limiting) sur l'API.
- Les captures d'écran du README sont des placeholders.
