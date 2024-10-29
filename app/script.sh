#!/bin/ash
set -e

echo "Waiting for database..."
python manage.py wait_for_db
echo "Apply database migrations"
python manage.py migrate
echo "Create default superuser"
python manage.py create_default_superuser
echo "Start the server"
python manage.py runserver 0.0.0.0:8000

exec "$@"