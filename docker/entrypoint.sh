#!/bin/sh
# Runs before the web server on every container start.
set -e

python manage.py migrate --noinput
python manage.py load_initial_data

exec "$@"
