# Deploying
Namubufferi can be deployed to heroku or packaged into a
docker container.

# Docker
## Local development
First, docker, docker-compose and docker-machine must be
installed.

While developing locally, we probably want to run docker
inside virtual machine. This is done by:

    docker-files/start_vm.sh
    eval $(docker-machine env namubufferi-vm)

After that, we can use docker-compose to setup our
development enviroment.

    docker-compose -f docker-files/docker-compose.yml -f docker-files/docker-compose.dev.yml up --build

If you make changes to static files, they must be updated
separately. (Ensure you are in the same shell you started
the vm from)

    docker-files/update_staticfiles.sh

Now namubufferi should be live in

    docker-machine ip namubufferi-vm

Admin user should also have been created with credentials:
_admin:password_

## In production
Docker image must be built with the build path being project
root.

While deploying the image, it will have static files in
`/static` and it will have gunicorn running in port 8080.

Make sure to setup relevant enviromental settings.

# Heroku
## Developing locally without docker
### 1. Install Postgres
#### Ubuntu/Debian
     Install PostgresSQL
     https://help.ubuntu.com/community/PostgreSQL#Alternative_Server_Setup
     https://devcenter.heroku.com/articles/heroku-postgresql#local-setup
    sudo apt-get install postgresql
    sudo apt-get install python-psycopg2
    sudo apt-get install libpq-dev
    sudo -u postgres createuser --superuser $USER
#### Mac
    https://devcenter.heroku.com/articles/heroku-postgresqlset-up-postgres-on-mac
### 2. Setup
    ./bin/setup
### 3. Run
    ./bin/run

## How to deploy?
* Checklist: https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/
* Create Heroku Account: https://www.heroku.com/

        heroku login
        heroku create *appname* --region eu
        heroku buildpacks:add -a *appname* heroku/nodejs
        heroku buildpacks:add -a *appname* heroku/python
        heroku config:set -a *appname* DEBUG=false NAMUBUFFERI_ALLOWEDHOSTS=\*
        git push heroku master
        heroku run ./bin/heroku-setup
