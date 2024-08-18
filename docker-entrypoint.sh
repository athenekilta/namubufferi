#!/bin/sh
set -eux

case "$1" in
  gunicorn)
    python manage.py collectstatic --noinput
  ;;
  *)
  ;;
esac

exec "$@"