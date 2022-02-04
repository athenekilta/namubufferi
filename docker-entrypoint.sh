#!/bin/sh
set -eux

case "$1" in
  gunicorn)
    pipenv run python manage.py collectstatic --noinput
  ;;
  *)
  ;;
esac

exec pipenv run "$@"
