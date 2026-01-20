#!/usr/bin/env sh
set -e

# ensure the sqlite file exists
mkdir -p /data
touch "${SQLITE_PATH:-/data/db.sqlite3}"

cd /app

python manage.py migrate --noinput

# if you use static (optional)
# python manage.py collectstatic --noinput

python manage.py runserver 0.0.0.0:8000
