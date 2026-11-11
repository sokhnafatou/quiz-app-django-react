"""
Commande de gestion : charge des données d'exemple fictives.

Utilisation :
    python manage.py load_sample_data

Crée deux quiz de démonstration :
- « Capitales d'Afrique »
- « Bases de Python »

La commande est idempotente : elle supprime les quiz existants dont le titre
correspond avant de les recréer, afin d'éviter les doublons.
"""

from django.core.management.base import BaseCommand

from quizzes.models import Choice, Question, Quiz


SAMPLE_DATA = [
    {
        "title": "Capitales d'Afrique",
        "description": "Testez vos connaissances sur les capitales des pays africains.",
        "questions": [
            {
                "text": "Quelle est la capitale du Sénégal ?",
                "choices": [
                    ("Bamako", False),
                    ("Dakar", True),
                    ("Conakry", False),
                    ("Abidjan", False),
                ],
            },
            {
                "text": "Quelle est la capitale du Nigeria ?",
                "choices": [
                    ("Lagos", False),
                    ("Kano", False),
                    ("Abuja", True),
                    ("Ibadan", False),
                ],
            },
            {
                "text": "Quelle est la capitale de l'Éthiopie ?",
                "choices": [
                    ("Addis-Abeba", True),
                    ("Asmara", False),
                    ("Djibouti", False),
                    ("Mogadiscio", False),
                ],
            },
            {
                "text": "Quelle est la capitale de l'Afrique du Sud (siège administratif) ?",
                "choices": [
                    ("Le Cap", False),
                    ("Johannesburg", False),
                    ("Durban", False),
                    ("Pretoria", True),
                ],
            },
            {
                "text": "Quelle est la capitale du Kenya ?",
                "choices": [
                    ("Mombasa", False),
                    ("Nairobi", True),
                    ("Kisumu", False),
                    ("Eldoret", False),
                ],
            },
        ],
    },
    {
        "title": "Bases de Python",
        "description": "Les fondamentaux du langage Python pour débutants.",
        "questions": [
            {
                "text": "Quel mot-clé permet de définir une fonction en Python ?",
                "choices": [
                    ("function", False),
                    ("def", True),
                    ("func", False),
                    ("define", False),
                ],
            },
            {
                "text": "Quel est le résultat de 7 // 2 en Python ?",
                "choices": [
                    ("3.5", False),
                    ("3", True),
                    ("4", False),
                    ("3.0", False),
                ],
            },
            {
                "text": "Quel type est utilisé pour stocker une séquence modifiable ?",
                "choices": [
                    ("tuple", False),
                    ("list", True),
                    ("str", False),
                    ("frozenset", False),
                ],
            },
            {
                "text": "Comment commente-t-on une ligne en Python ?",
                "choices": [
                    ("// commentaire", False),
                    ("# commentaire", True),
                    ("/* commentaire */", False),
                    ("-- commentaire", False),
                ],
            },
            {
                "text": "Quelle méthode ajoute un élément à la fin d'une liste ?",
                "choices": [
                    ("list.add()", False),
                    ("list.push()", False),
                    ("list.append()", True),
                    ("list.insert()", False),
                ],
            },
        ],
    },
]


class Command(BaseCommand):
    help = "Charge des quiz et questions d'exemple fictifs."

    def handle(self, *args, **options):
        created_quizzes = 0
        created_questions = 0
        created_choices = 0

        for data in SAMPLE_DATA:
            # Idempotence : on supprime un quiz de même titre s'il existe.
            Quiz.objects.filter(title=data["title"]).delete()
            quiz = Quiz.objects.create(
                title=data["title"],
                description=data["description"],
            )
            created_quizzes += 1

            for order, question_data in enumerate(data["questions"]):
                question = Question.objects.create(
                    quiz=quiz,
                    text=question_data["text"],
                    order=order,
                )
                created_questions += 1
                for text, is_correct in question_data["choices"]:
                    Choice.objects.create(
                        question=question,
                        text=text,
                        is_correct=is_correct,
                    )
                    created_choices += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Données d'exemple chargées : "
                f"{created_quizzes} quiz, {created_questions} questions, "
                f"{created_choices} choix."
            )
        )
