import json

import pytest
import requests

import config.config as config
from project import BahnAPI
import tests.data.data_tests as data_tests


@pytest.fixture
def bahnapi_object():
    ba = BahnAPI.BahnAPI()
    ba.access_token = data_tests.token
    ba._set_headers()
    return ba


@pytest.fixture
def bahn_fake_api(monkeypatch):

    class FakeBahnAPI:

        def __init__(self, url, **kwargs):
            if url == config.URLS['base'] + config.URLS['betriebsstellen']:
                try:
                    assert 'params' in kwargs.keys()
                    assert 'headers' in kwargs.keys()

                    params = kwargs['params']
                    assert 'name' in params.keys()
                    assert params['name'] == data_tests.bahnhof

                    headers = kwargs['headers']
                    assert 'Accept' in headers.keys()
                    assert 'Authorization' in headers.keys()
                    assert headers['Accept'] == 'application/json'
                    assert headers['Authorization'] == 'Bearer ' + data_tests.token
                    self.status_code = 200
                    self.content = json.dumps(data_tests.betriebsstelle_response)
                except AssertionError:
                    self.status_code = 404
                    self.content = {'error': 'error'}
            # TODO test for generic cases
            elif url == config.URLS['base'] + config.URLS['station'] + data_tests.bahnhof_abbrev:
                try:
                    assert 'headers' in kwargs.keys()
                    headers = kwargs['headers']
                    assert 'Accept' in headers.keys()
                    assert 'Authorization' in headers.keys()
                    assert headers['Accept'] == 'application/xml'
                    assert headers['Authorization'] == 'Bearer ' + data_tests.token
                    self.status_code = 200
                    self.content = data_tests.eva_number_response_content
                except AssertionError:
                    self.status_code = 404
                    # TODO content in error case?
                    self.content = {'error': 'error'}
            elif url == config.URLS['base'] + config.URLS['default_plan'] + '8000086/190124/23':
                try:
                    self.status_code = 200
                except AssertionError:
                    self.status_code = 404
                    self.content = {'error': 'error'}
            else:
                self.status_code = 404
                self.content = {'error': 'error'}

        def json(self):
            return json.loads(self.content)

    monkeypatch.setattr(requests, 'get', FakeBahnAPI)


def test_bahnapi(bahnapi_object):
    assert bahnapi_object.headers_json
    assert bahnapi_object.headers_xml
    assert bahnapi_object.urls == config.URLS
    assert bahnapi_object.access_token

    assert 'Accept' in bahnapi_object.headers_json.keys()
    assert 'Authorization' in bahnapi_object.headers_json.keys()
    assert bahnapi_object.headers_json['Accept'] == 'application/json'
    assert 'Bearer' in bahnapi_object.headers_json['Authorization']

    assert 'Accept' in bahnapi_object.headers_xml.keys()
    assert 'Authorization' in bahnapi_object.headers_xml.keys()
    assert bahnapi_object.headers_xml['Accept'] == 'application/xml'
    assert 'Bearer' in bahnapi_object.headers_xml['Authorization']


def test_bahnapi__get_url(bahnapi_object):
    assert bahnapi_object._get_url('/a/') == config.URLS['base'] + '/a/'
    assert bahnapi_object._get_url('/a/', 'b') == config.URLS['base'] + '/a/' + 'b'
    assert bahnapi_object._get_url('/a/', 'bc') == config.URLS['base'] + '/a/' + 'bc'
    assert bahnapi_object._get_url('/a/', ['b', 'c']) == config.URLS['base'] + '/a/' + 'b' + '/' + 'c'


def test_bahnapi__request(bahnapi_object, bahn_fake_api):
    # TODO test for errors
    assert False


def test_bahnapi_get_betriebsstelle(bahnapi_object, bahn_fake_api):
    # TODO test for errors
    assert bahnapi_object._get_betriebsstelle(data_tests.bahnhof) == data_tests.betriebsstelle_response


def test_bahnapi_get_eva_number(bahnapi_object, bahn_fake_api):
    # TODO test for errors
    assert bahnapi_object.get_eva_number(data_tests.bahnhof_abbrev) == data_tests.eva_number


def test_bahnapi_get_default_plan(bahnapi_object, bahn_fake_api):
    assert False


def test_bahnapi_get_bahnhof_abbrev(bahnapi_object, bahn_fake_api):
    assert bahnapi_object.get_bahnhof_abbrev(data_tests.bahnhof) == data_tests.bahnhof_abbrev


def test_bahnapi__extract_bahnhof_abbrev(bahnapi_object):
    # TODO test for errors
    assert bahnapi_object._extract_bahnhof_abbrev(data_tests.betriebsstelle_response) == data_tests.bahnhof_abbrev


def test_bahnapi__extract_eva_number(bahnapi_object):
    # TODO test for errors
    assert bahnapi_object._extract_eva_number(data_tests.eva_number_response_content) == data_tests.eva_number
