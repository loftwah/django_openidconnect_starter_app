# Django OpenID Connect with Deauthorized Example

- This is a sample Django 2.0 app that uses OpenID Connect with the Deauthorized server.
- We built this for new users to ramp up quickly and test out the functionality for biometric authentication.
- This app also serves as a basic blueprint for intergation with your apps for development.  


## Deploy sample app to Heroku

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)


## Default ENV variables

The following variables will be loaded by default into your heroku config when you hit the deploy button. These variables will not change unless you are running your own instance of the server using docker or our enteprise tier.

```
"OPENID_HOST"="srv0.qryp.to"
"OPENID_PORT"="443"
"OPENID_ISSUER"="https://srv0.qryp.to:8002/op" 
```


## Create an account

Create an account or login to the Deauthorized Dashboard to provision a OPENID_CLIENT_ID and OPENID_CLIENT_SECRET for this app.

* Login or create an account on the dashboard https://www.deauthorized.com/users/sign_up
* Click on the applicaitons tab and then add an application


## Provision the OPENID_CLIENT_ID and OPENID_CLIENT_SECRET for the app

Fill out the application form to add the domain, type of application, and the callback URL

* Set your domain from the Heroku config http://mydomain.herokuapp.com
* Select the 'web' platform
* Add the callback URL. In this case use http://mydomain.herokuapp.com/openid_auth_callback

This should yield a set of configuration values that provisions your app with the identity server. NOTE - You cannot edit the callback URL, so if you add the wrong callback URL, you will need to delete your OpenID client app and provision another one with the correct callback URL.


### Example OpenID Client Connection Configuration:

```
OpenID Client ID: 0d2ee26a-e0d6-4b91-aded-1ef0618f62c2 ## This is the OPENID_CLIENT_ID
OpenID Client Secret: dvEJSuG3Y8DYS/hcaxEKigYK25WeYCOgxCJLDH3EpH/vUI1X1hzSErDlNfLID9aP  ## This is the OPENID_CLIENT_SECRET
OpenID Host: srv.qryp.to
OpenID Port: 443
OpenID Issuer: https://srv.qryp.to/op
```


## Add your config ENV variables from the Deauthroized dashboard to the Heroku settings tab

Take the OPENID_CLIENT_ID and OPENID_CLIENT_SECRET you provisioned from the dashboard and set them in Heroku under the settings tab.

```
"OPENID_CLIENT_ID"="0d2ee26a-e0d6-4b91-aded-1ef0618f62c2" 
"OPENID_CLIENT_SECRET"="dvEJSuG3Y8DYS/hcaxEKigYK25WeYCOgxCJLDH3EpH/vUI1X1hzSErDlNfLID9aP" 
```


## Documentation

For more information on using Deauthorized's biometric authentication solutions, [visit our website](https://www.deauthorized.com)
