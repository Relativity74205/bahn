import json

import requests

import config.config as config


class BahnAPI:

    def __init__(self):
        self.headers_json = None
        self.headers_xml = None
        self.urls = config.URLS

        self._set_headers()

    def _request(self, method, url, **kwargs):
        try:
            r = method(url, **kwargs)
        except ConnectionError:
            print("URL wrong")
            raise

        if r.status_code != 200:
            print(f"status_code: {r.status_code}")
            print(r.content)
            print(json.dumps(r.json(), indent=4))
            raise ConnectionError

        return r

    def get_betriebsstelle(self, bahnhof):
        data = {'name': bahnhof}
        url = self._get_url(self.urls['betriebsstellen'])

        r = self._request(requests.get, url, headers=self.headers_json, params=data)

        return r.json()

    def get_eva_number(self, edg):
        url = self._get_url(self.urls['station'], suffix=[edg])

        r = self._request(requests.get, url, headers=self.headers_xml)

        return r

    def get_default_plan(self, eva, date, hour):
        url = self._get_url(self.urls['default_plan'], suffix=[eva, date, hour])

        r = self._request(requests.get, url, headers=self.headers_xml)

        return r

    def _set_headers(self):
        self.headers_json = {'Accept': 'application/json',
                             'Authorization': 'Bearer ' + config.access_token}
        self.headers_xml = {'Accept': 'application/xml',
                            'Authorization': 'Bearer ' + config.access_token}

    def _get_url(self, url_part, suffix=()):
        if type(suffix) is str:
            return self.urls['base'] + url_part + suffix
        else:
            return self.urls['base'] + url_part + '/'.join(suffix)
