# Namubufferi

## Prerequisites

- https://docs.docker.com/

## Development

    ./createsecrets.py
    docker compose run --rm web ./init.sh
    docker compose up

- Django
  - http://localhost:8000/
- Mailhog (email testing)
  - http://localhost:8025/
- React development
  - http://localhost:3000/

## Deployment

- https://docs.djangoproject.com/en/3.2/howto/deployment/
- https://docs.docker.com/compose/extends/#multiple-compose-files
- https://devcenter.heroku.com/articles/build-docker-images-heroku-yml
