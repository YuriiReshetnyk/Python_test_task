#!/bin/ash
set -e

echo "Waiting for database..."
python manage.py wait_for_db
echo "Waiting 30 seconds for migrations to be applied"
sleep 30

exec "$@"