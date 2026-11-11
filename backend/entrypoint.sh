#!/bin/sh
# Point d'entrée du conteneur backend.
# Applique les migrations, charge les données d'exemple, puis lance le serveur.

set -e

echo "Application des migrations Django..."
python manage.py migrate --noinput

echo "Chargement des données d'exemple..."
python manage.py load_sample_data

echo "Collecte des fichiers statiques..."
python manage.py collectstatic --noinput

exec "$@"
