# Namubufferi

## Prerequisites

- https://docs.docker.com/
- Easiest option is to install docker destkop

## Development

Run
`./createsecrets.py` to generate django & postgres passwords.
`docker compose run --rm web ./init.sh`
`docker compose up`

- Django
  - http://localhost:8081/
- Mailhog (email testing)
  - http://localhost:8025/
- React development
  - http://localhost:3000/

### Accessing the container command line and creating a superuser
```bash
docker exec -it namubufferi-web-1 bash # replace namubuffa_web_1 with the actual name of the container
# you should now be working inside the container and greeted by a command line ending in `#` character
python manage.py createsuperuser
```
Answer questions and log in at `/admin` to view the admin panel.

## Deployment

- https://docs.djangoproject.com/en/3.2/howto/deployment/
- https://docs.docker.com/compose/extends/#multiple-compose-files
- https://devcenter.heroku.com/articles/build-docker-images-heroku-yml
