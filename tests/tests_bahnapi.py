import json

import pytest
import requests

import config.config as config
import BahnAPI


@pytest.fixture
def bahnapi_object():
    return BahnAPI.BahnAPI()


@pytest.fixture
def bahn_fake_api(monkeypatch):

    class FakeBahnAPI:

        def __init__(self, url, **kwargs):
            if url == config.URLS['base'] + config.URLS['betriebsstellen']:
                pass
            elif url == config.URLS['base'] + config.URLS['station'] + 'EDG':
                pass
            elif url == config.URLS['base'] + config.URLS['default_plan'] + '8000086/190124/23':
                pass
            else:
                self.status_code = 404
                self.content = {'error': 'error'}

        def json(self):
            return json.dumps(self.content)

    monkeypatch.setattr(requests, 'get', FakeBahnAPI)


def test_bahnapi(bahnapi_object):
    assert bahnapi_object.headers_json
    assert bahnapi_object.headers_xml
    assert bahnapi_object.urls == config.URLS

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


def test_bahnapi__request(bahn_fake_api):
    assert False


def test_bahnapi_get_betriebsstelle(bahn_fake_api):
    assert False


def test_bahnapi_get_eva_number(bahn_fake_api):
    assert False


def test_bahnapi_get_default_plan(bahn_fake_api):
    assert False
