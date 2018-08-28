Some helpful commands for doing development on the Django / Python sample:
-----------

## Deploy sample app to Heroku

```sh
$ heroku create
$ git push heroku master

$ heroku run python manage.py migrate
$ heroku open
```

## Run sample app locally
```sh
$ git clone git@github.com:Deauthorized/python_openidconnect_starter_app.git
$ cd python_openidconnect_starter_app

# Setup Environment
$ pipenv install

# OR

$ conda env create && source activate deauthorized-python-sample

$ createdb python_getting_started

$ python manage.py migrate
$ python manage.py collectstatic

# Run dev server
$ heroku local
```
