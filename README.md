# Namubufferi Alpha
Test app @ https://namubufferi.herokuapp.com/

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

## Or, Develop with docker
#### Notes
When running update_code.sh, ensure you are in project root.

### Create a new development vm
  docker-machine create -d virtualbox namubufferi-vm
  eval $(docker-machine env namubufferi-vm)
  eval $(ssh-agent)
  ssh-add ~/.docker/machine/machines/namubufferi-vm/id_rsa
  docker-machine ssh namubufferi-vm -- tce-load -wi rsync
  ./docker-files/update_code.sh

### After that, build containers and run them
  docker-compose -f docker-files/docker-compose.yml -f docker-files/docker-compose.dev.yml  up --build

### Using
  Navigate to vm ip (docker-machine ip namubufferi-vm)
  After making alternations to code, run docker-files/update_code.sh

Having project as a volume in development makes updating changes faster, but
has one drawback: code won't update when rebuilding container and you have
to manually run update_code.sh before rebuild.


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
