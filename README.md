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
### 1. Install Postgres
#### Ubuntu/Debian
    # Install PostgresSQL
    # https://help.ubuntu.com/community/PostgreSQL#Alternative_Server_Setup
    # https://devcenter.heroku.com/articles/heroku-postgresql#local-setup
    sudo apt-get install postgresql
    sudo apt-get install python-psycopg2
    sudo apt-get install libpq-dev
    sudo -u postgres createuser --superuser $USER
#### Mac
    https://devcenter.heroku.com/articles/heroku-postgresql#set-up-postgres-on-mac
### 2. Setup
    ./bin/setup
### 3. Run
    ./bin/run

## How to deploy?
### Heroku:
* Checklist: https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/
* Create Heroku Account: https://www.heroku.com/

        heroku login
        heroku create *appname* --region eu  
        git push heroku master
        heroku run ./bin/heroku-setup

### Apache:
* Checklist: https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/
* https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/modwsgi/
