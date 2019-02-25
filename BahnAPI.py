import json
import html

import requests
import xmltodict

import config.config_credentials as credentials
import config.config as config


class BahnAPI:

    def __init__(self):
        self.headers_json = None
        self.headers_xml = None
        self.urls = config.URLS
        self.access_token = credentials.access_token

        self._set_headers()

    @staticmethod
    def _request(method, url, **kwargs):
        try:
            r = method(url, **kwargs)
        except requests.exceptions.RequestException:
            print("URL wrong")
            # TODO logging
            # TODO error handling
            raise

        if r.status_code != 200:
            # TODO logging
            print(f"status_code: {r.status_code}")
            print(r.content)
            if r.status_code == 410:
                print('Date is in the past')
            try:
                print(json.dumps(r.json(), indent=4))
            except ValueError:
                print('no json')
            raise requests.exceptions.RequestException

        return r

    def get_bahnhof_abbrev(self, bahnhof):
        betriebsstelle = self._get_betriebsstelle(bahnhof)
        bahnhof_abbrev = self._extract_bahnhof_abbrev(betriebsstelle)

        return bahnhof_abbrev

    @staticmethod
    def _extract_bahnhof_abbrev(betriebsstelle):
        try:
            bahnhof_abbrev = betriebsstelle[0]['abbrev']
        except KeyError:
            # TODO logging
            raise
        except TypeError:
            # TODO logging
            raise

        return bahnhof_abbrev

    def _get_betriebsstelle(self, bahnhof):
        data = {'name': bahnhof}
        url = self._get_url(self.urls['betriebsstellen'])

        r = self._request(requests.get, url, headers=self.headers_json, params=data)

        return r.json()

    def get_eva_number(self, station):
        url = self._get_url(self.urls['station'], suffix=[station])

        r = self._request(requests.get,
                          url,
                          headers=self.headers_xml)
        eva_number = self._extract_eva_number(r.content)

        return eva_number

    @staticmethod
    def _extract_eva_number(content):
        # TODO error handling for xml to utf-8
        r_json = xmltodict.parse(content.decode('utf-8'))
        try:
            eva_number = r_json['stations']['station']['@eva']
        except KeyError:
            # TODO logging
            raise

        return eva_number

    def get_default_plan(self, eva: str, date: str, hour: str) -> str:
        url = self._get_url(self.urls['default_plan'], suffix=[eva, date, hour])

        r = self._request(requests.get, url, headers=self.headers_xml)
        r_content = self._extract_default_plan(r)

        return r_content

    @staticmethod
    def _extract_default_plan(response: requests.Response) -> str:
        # TODO exception handling
        response_content = html.unescape(response.content.decode('utf-8'))

        return response_content

    def get_full_changes(self, eva):
        url = self._get_url(self.urls['full_changes'], suffix=[eva])
        print(url)

        r = self._request(requests.get, url, headers=self.headers_xml)

        return r

    def get_recent_changes(self, eva):
        url = self._get_url(self.urls['recent_changes'], suffix=[eva])

        r = self._request(requests.get, url, headers=self.headers_xml)

        return r

    def _set_headers(self):
        self.headers_json = {'Accept': 'application/json',
                             'Authorization': 'Bearer ' + self.access_token}
        self.headers_xml = {'Accept': 'application/xml',
                            'Authorization': 'Bearer ' + self.access_token}

    def _get_url(self, url_part, suffix=()):
        if type(suffix) is str:
            return self.urls['base'] + url_part + suffix
        else:
            return self.urls['base'] + url_part + '/'.join(suffix)
