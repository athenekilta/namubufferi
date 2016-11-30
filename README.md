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
### Setup
    ./setup.sh
### Run
    ./run.sh

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

