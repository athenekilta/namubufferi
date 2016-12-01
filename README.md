# Namubufferi Alpha
Test app @ https://namupankki.herokuapp.com/

## TODOs
* UI Facelift, it still is all default Bootstrap Paper and looks like shit.
* Too much modals
* Refactor
    * There's some dead code that could be removed
    * Split namubufferiapp to smaller reusable apps
    * ...

## How to dev?
### Install Postgres
#### Ubuntu/Debian
    # Install PostgresSQL
    # https://help.ubuntu.com/community/PostgreSQL#Alternative_Server_Setup
    # https://devcenter.heroku.com/articles/heroku-postgresql#local-setup
    sudo apt-get install postgresql
    sudo apt-get install python-psycopg2
    sudo apt-get install libpq-dev
    sudo -u postgres createuser --superuser $USER
#### Other
    https://devcenter.heroku.com/articles/heroku-postgresql#local-setup
### Setup
    ./bin/setup
### Run
    ./bin/run

## How to deploy?
### Heroku:
* `git checkout heroku`
* Checklist: https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/
* Create Heroku Account: https://www.heroku.com/

        heroku login
        heroku create *appname* --region eu  
        git push heroku heroku:master

### Apache:
* Checklist: https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/
* https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/modwsgi/
