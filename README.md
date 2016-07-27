# Namupankki
Test app @:  
https://namupankki.herokuapp.com/

## How to dev?
### Build
    ./build.sh
### Run
    ./run.sh

## How to deploy?
### Apache:
* Checklist: https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/
* https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/modwsgi/


### Heroku:
* `git checkout heroku`
* Checklist: https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/
* Create Heroku Account: https://www.heroku.com/

        heroku login
        heroku create *appname* --region eu  
        git push heroku heroku:master
