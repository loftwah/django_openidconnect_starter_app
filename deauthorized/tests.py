from unittest import mock

from django.test import TestCase, RequestFactory

from deauthorized.views import index
from deauthorized.views import auth
from deauthorized.views import auth_callback


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
        resp = dict(access_token='fill in access token',
                    id_token='fill in id token')
        return MockResponse(resp, 200)
    else:
        raise ValueError('Not sure how to mock url:{}'.format(requested_url))


class SimpleTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_index_view(self):
        request = self.factory.get('/')
        response = index(request)
        assert response.status_code == 200

    def test_auth_view(self):
        request = self.factory.get('/auth')
        response = auth(request)
        assert response.status_code == 302

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    @mock.patch('requests.post', side_effect=mocked_requests_post)
    def test_auth_callback_view(self, mock_post, mock_get):
        request_params = {'code': 'test', 'state': 'test'}
        request = self.factory.get('/openid_auth_callback', request_params)
        response = auth_callback(request)
        assert response.status_code == 200
        assert 'text/html' in response.get('content-type')
