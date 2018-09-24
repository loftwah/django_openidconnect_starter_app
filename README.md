# Django OpenID Connect with Deauthorized Example
[![Build Status](https://travis-ci.org/Deauthorized/django_openidconnect_starter_app.svg?branch=master)](https://travis-ci.org/Deauthorized/django_openidconnect_starter_app) [![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/Deauthorized/django_openidconnect_starter_app/)
--------

- This is a sample Django 2.0 app that uses OpenID Connect with the Deauthorized server.
- This app also serves as a basic blueprint for intergation with your apps for development.  


## Create a Deauthorized Application

1. Sign up to the Deauthorized Beta
2. Log into Deauthorized Dashboard
3. Create a new application from Applications tab

With your application provisioned, you will have the necessary `OPENID_CLIENT_ID` and `OPENID_CLIENT_SECRET` to launch the sample application.

```sh
OpenID Client ID: 0d2ee26a-e0d6-4b91-aded-1ef0618f62c2 ## This is the OPENID_CLIENT_ID
OpenID Client Secret: dvEJSuG3Y8DYS/hcaxEKigYK25WeYCOgxCJLDH3EpH/vUI1X1hzSErDlNfLID9aP  ## This is the OPENID_CLIENT_SECRET
OpenID Issuer: https://srv.qryp.to/op
```

## Deploy Sample Application

Heroku is the fastest way to get the sample app running.

### Single Click Heroku Deployment

1. Deploy by clicking Heroku deploy button above

2. Update `OPENID_CLIENT_ID` and `OPENID_CLIENT_SECRET` environment vars with you with those you provisioned in the Deauthorized dashboard.

### Manual Heroku Deployment

To experiment with making edits to the sample application:

1. Clone sample application locally

```sh
git clone https://github.com/Deauthorized/django_openidconnect_starter_app
cd django_openidconnect_starter_app
```

2. Create Heroku Application:

```sh
heroku create --app deauthorized-django-sample
git config --list | grep heroku
git push heroku master
```

3. Make your code updates in [`deauthorized/views.py`](https://github.com/Deauthorized/django_openidconnect_starter_app/blob/master/deauthorized/views.py)

```sh
git add deauthorized/views.py
git commit -m 'small update to sample app'
git push heroku master
heroku run python manage.py migrate
heroku open
```

## Documentation

For more information on using Deauthorized's biometric authentication solutions, [visit our website](https://www.deauthorized.com)


## Running Tests

This sample includes a test suite to help with customization and development.

To run the tests, open a terminal to the sample project directory and run:
```sh
pytest -sv
```


## Running using Docker & Docker Compose

Assuming you have an update version of `Docker` installed, the following commands will help you run the sample app:

1. Clone the example repo and browse to the root:

```bash
git clone https://github.com/Deauthorized/django_openidconnect_starter_app
cd django_openidconnect_starter_app
docker-compose up --build
```

2. Update the `.env` file with the `OPENID_CLIENT_ID` and `OPENID_CLIENT_SECRET` which you obtain while provisioning your application.

3. Use docker compose to build and launch the container

```bash
docker-compose up --build
```
