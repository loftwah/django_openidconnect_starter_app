from os import environ
from base64 import b64decode

import json
from django.http import JsonResponse, HttpResponseBadRequest
from django.utils.http import urlencode

from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse

from oic.oic import Client
from oic.utils.authn.client import CLIENT_AUTHN_METHOD
from oic import rndstr

from jwkest.jwk import load_jwks_from_url
from jwkest.jwk import SYMKey
from jwkest.jws import JWS

import requests

import logging

logger = logging.getLogger(__name__)


OPENID_ISSUER = environ.get('OPENID_ISSUER', 'https://srv.qryp.to/op')
OPENID_CLIENT_ID = environ.get('OPENID_CLIENT_ID', 'deauthorized')
OPENID_CLIENT_SECRET = environ.get('OPENID_CLIENT_SECRET', '123')
SCOPES_SUPPORTED = ['openid', 'email', 'profile', 'address']

client = Client(client_authn_method=CLIENT_AUTHN_METHOD)
provider_info = client.provider_config(OPENID_ISSUER)
auth_endpoint = provider_info['authorization_endpoint']
token_endpoint = provider_info['token_endpoint']
userinfo_endpoint = provider_info['userinfo_endpoint']
end_session_endpoint = provider_info['end_session_endpoint']
revocation_endpoint = provider_info['revocation_endpoint']

jwks_uri = provider_info['jwks_uri']


def logout(request):

    # get logout url from end_session_endpoint

    # params = {
    #     'grant_type': 'authorization_code',
    #     'code': response['code'],
    #     'redirect_uri': redirect_uri
    # }

    # openid_auth = (OPENID_CLIENT_ID, OPENID_CLIENT_SECRET)
    # access_token_response = requests.post(end_session_endpoint,
    #                                       auth=openid_auth,
    #                                       data=params)
    # try:
    #     access_token_response.raise_for_status()
    # except:
    #     return JsonResponse({'message': 'error during access token request'})
    pass


def index(request):
    return render(request, 'index.html')


def auth(request):
    global auth_endpoint

    session_info = {}
    session_info['state'] = rndstr()
    session_info['nonce'] = rndstr()

    redirect_uri = 'https://{}{}'.format(request.get_host(),
                                         reverse('openid_auth_callback'))
    params = {
        'response_type': 'code',
        'state': session_info['state'],
        'nonce': session_info['nonce'],
        'client_id': OPENID_CLIENT_ID,
        'redirect_uri': redirect_uri,
        'scope': ' '.join(SCOPES_SUPPORTED)
    }

    return redirect(auth_endpoint + '?' + urlencode(params))


def auth_callback(request):
    '''
    '''
    global sessions
    global token_endpoint
    global userinfo_endpoint
    global provider_info

    response = request.GET

    if 'code' not in response or 'state' not in response:
        return HttpResponseBadRequest('Invalid request')

    redirect_uri = 'https://{}{}'.format(request.get_host(),
                                         reverse('openid_auth_callback'))

    # get access token
    params = {
        'grant_type': 'authorization_code',
        'code': response['code'],
        'redirect_uri': redirect_uri
    }

    openid_auth = (OPENID_CLIENT_ID, OPENID_CLIENT_SECRET)
    access_token_response = requests.post(token_endpoint,
                                          auth=openid_auth,
                                          data=params)
    try:
        access_token_response.raise_for_status()
    except:
        return JsonResponse({'message': 'error during access token request'})

    access_json = access_token_response.json()
    access_token = access_json['access_token']

    id_token = access_json['id_token']
    if not id_token:
        return JsonResponse({'message': 'null id token in access response'})

    # get userinfo token
    user_response = requests.get(userinfo_endpoint, headers={
        'Authorization': 'Bearer {}'.format(access_token)
    })

    if user_response.status_code != 200:
        return HttpResponseBadRequest('Invalid User Info Response')

    # stub in missing props
    user_json = user_response.json()

    if 'name' not in user_json:
        user_json['name'] = user_json['sub']

    if 'nickname' not in user_json:
        user_json['nickname'] = 'nickname'

    if 'email' not in user_json:
        user_json['email'] = 'email'

    if 'email_verified' not in user_json:
        user_json['email_verified'] = 'email_verified'

    if 'updated_at' not in user_json:
        user_json['updated_at'] = 'updated_at'

    return render(request, 'profile.html', user_json)


def verify_id(token):
    global jwks_uri

    header, claims, signature = token.split('.')
    header = b64d(header)
    claims = b64d(claims)

    if not signature:
        raise ValueError('Invalid Token')

    if header['alg'] not in ['HS256', 'RS256']:
        raise ValueError('Unsupported signing method')

    if header['alg'] == 'RS256':
        signing_keys = load_jwks_from_url(jwks_uri)
    else:
        signing_keys = [SYMKey(key=str(OPENID_CLIENT_SECRET))]

    id_token = JWS().verify_compact(token, signing_keys)
    id_token['header_info'] = header
    return id_token


def b64d(token):
    token += ('=' * (len(token) % 4))
    decoded = b64decode(token)
    return json.loads(decoded)
