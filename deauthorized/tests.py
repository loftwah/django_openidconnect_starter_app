from unittest import mock

from django.test import TestCase, RequestFactory


from deauthorized.views import index
from deauthorized.views import auth

from django.contrib.auth import get_user_model
from django.test.client import Client

User = get_user_model()


MOCK_ID_TOKEN = 't' * 1024
MOCK_ACCESS_TOKEN = 'a' * 256


class MockResponse:

    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data

    def raise_for_status(self):
        pass


def mocked_requests_get(*args, **kwargs):
    requested_url = args[0]
    if 'op/me' in requested_url:
        resp = dict(name='test',
                    nickname='test',
                    email='test',
                    email_verified='test',
                    updated_at='test')
        return MockResponse(resp, 200)
    else:
        raise ValueError('Not sure how to mock url:{}'.format(requested_url))


def mocked_requests_post(*args, **kwargs):

    requested_url = args[0]
    if 'token' in requested_url:
        resp = dict(access_token=MOCK_ACCESS_TOKEN,
                    id_token=MOCK_ID_TOKEN)
        return MockResponse(resp, 200)
    else:
        raise ValueError('Not sure how to mock url:{}'.format(requested_url))


class DeauthorizedTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()

    def test_index_view(self):
        request = self.factory.get('/')
        response = index(request)
        assert response.status_code == 200

    def test_auth_view(self):
        request = self.factory.get('/auth')
        response = auth(request)
        assert response.status_code == 302

    def test_logout_view(self):
        user_params = dict(id_token=MOCK_ID_TOKEN,
                           access_token=MOCK_ACCESS_TOKEN)
        user, created = User.objects.get_or_create(**user_params)
        user.set_unusable_password()
        user.save()
        self.client.force_login(user)
        logout_response = self.client.get('/logout')
        assert logout_response.status_code == 302
        assert MOCK_ID_TOKEN in logout_response.url

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    @mock.patch('requests.post', side_effect=mocked_requests_post)
    def test_auth_callback_view(self, mock_post, mock_get):
        request_params = {'code': 'test', 'state': 'test'}
        response = self.client.get('/openid_auth_callback', request_params)
        assert response.status_code == 200
        assert 'text/html' in response.get('content-type')

        user = User.objects.get(id_token=MOCK_ID_TOKEN)
        assert user is not None
        assert user.id_token == MOCK_ID_TOKEN
        assert user.access_token == MOCK_ACCESS_TOKEN

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    @mock.patch('requests.post', side_effect=mocked_requests_post)
    def test_auth_callback_creates_user(self, mock_post, mock_get):
        request_params = {'code': 'test', 'state': 'test'}
        response = self.client.get('/openid_auth_callback', request_params)
        assert response.status_code == 200
        assert 'text/html' in response.get('content-type')

        user = User.objects.get(id_token=MOCK_ID_TOKEN)
        assert user is not None
        assert user.id_token == MOCK_ID_TOKEN
        assert user.access_token == MOCK_ACCESS_TOKEN

    def test_user_get_or_create(self):
        token = 'asdf'
        user, _ = User.objects.get_or_create(id_token='asdf')
        assert user is not None
        assert user.id_token == token
        assert user.access_token is None
