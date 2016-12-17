# Namubufferi

Alpha

## Development

    ./bin/setup
    ./bin/run

## Heroku Local

- https://devcenter.heroku.com/articles/heroku-postgresql#local-setup

---

    ./bin/heroku-local-setup
    ./bin/heroku-local

## Heroku Deployment

- https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

---

    heroku login
    heroku create $appname --region eu
    git push heroku master
    heroku run ./bin/heroku-setup
