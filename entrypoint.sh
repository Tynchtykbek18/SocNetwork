#!/bin/sh

# Apply migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --no-input

celery -A config worker -l info --without-gossip --without-mingle --without-heartbeat &
# Start Gunicorn server
exec gunicorn --bind :8000 config.wsgi:application