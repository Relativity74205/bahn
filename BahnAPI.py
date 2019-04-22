import json
import html
import logging
from typing import List, Dict
import xml

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
        except requests.exceptions.RequestException as e:
            msg = f'Request failed, probably wrong url; error_msg: {str(e)}'
            raise Exception(msg) from e

        return r

    def get_bahnhof_abbrev(self, bahnhof):
        betriebsstelle = self._get_betriebsstelle(bahnhof)
        bahnhof_abbrev = self._extract_bahnhof_abbrev(betriebsstelle, bahnhof)

        return bahnhof_abbrev

    @staticmethod
    def _extract_bahnhof_abbrev(betriebsstelle: List[Dict], bahnhof: str) -> str:
        bahnhof_abbrev = None
        try:
            for entry in betriebsstelle:
                if entry['name'] == bahnhof:
                    bahnhof_abbrev = entry['abbrev']
        except KeyError as e:
            logging.critical(f'KeyError during _extract_bahnhof_abbrev; error_msg: {str(e)}')
            bahnhof_abbrev = None
        except TypeError as e:
            logging.critical(f'TypeError during _extract_bahnhof_abbrev; error_msg: {str(e)}')
            bahnhof_abbrev = None

        return bahnhof_abbrev

    def _get_betriebsstelle(self, bahnhof):
        data = {'name': bahnhof}
        url = self._get_url(self.urls['betriebsstellen'])

        r = self._request(requests.get, url, headers=self.headers_json, params=data)
        try:
            r_json = r.json()
        except ValueError:
            r_json = None
            logging.critical('Response from _get_betriebsstelle has no json')

        return r_json

    def get_eva_number(self, station: str) -> str:
        url = self._get_url(self.urls['station'], suffix=[station])

        r = self._request(requests.get, url, headers=self.headers_xml)
        eva_number = self._extract_eva_number(r)

        return eva_number

    def _extract_eva_number(self, r: requests.Response) -> str:
        r_json = self._xml_content_to_json(r)
        try:
            eva_number = r_json['stations']['station']['@eva']
        except KeyError as e:
            logging.critical(f'Extracting EVA number from json failed; '
                             f'json_dumps {json.dumps(r_json)}; error_msg: {str(e)}')
            eva_number = None

        return eva_number

    # TODO refactor get_default_plan, get_full_changes and get_recent_changes into one
    def get_default_plan(self, eva: str, date: str, hour: str) -> Dict:
        url = self._get_url(self.urls['default_plan'], suffix=[eva, date, hour])

        r = self._request(requests.get, url, headers=self.headers_xml)
        self._log_status_code(r, 'get_default_plan')
        if r.status_code != 200:
            r_json = None
        else:
            r_json = self._xml_content_to_json(r)

        return r_json

    def get_full_changes(self, eva: str) -> Dict:
        url = self._get_url(self.urls['full_changes'], suffix=[eva])

        r = self._request(requests.get, url, headers=self.headers_xml)
        self._log_status_code(r, 'get_full_changes')
        if r.status_code != 200:
            r_json = None
        else:
            r_json = self._xml_content_to_json(r)

        return r_json

    def get_recent_changes(self, eva: str) -> Dict:
        url = self._get_url(self.urls['recent_changes'], suffix=[eva])

        r = self._request(requests.get, url, headers=self.headers_xml)
        self._log_status_code(r, 'get_recent_changes')
        if r.status_code != 200:
            r_json = None
        else:
            r_json = self._xml_content_to_json(r)

        return r_json

    @staticmethod
    def _log_status_code(r, f_name: str) -> None:
        if r.status_code != 200:
            logging.critical(f'Response from {f_name}-request has not status_code 200; '
                             f'status_code is {r.status_code}; content is {r.content}')
            if r.status_code == 410:
                logging.critical(f'{f_name}-request failed probably due to date is in the past')
            elif r.status_code == 400:
                logging.critical(f'{f_name}-request failed probably due to incorrect EVA number')
            elif r.status_code == 404:
                logging.critical(f'{f_name}-request failed probably due to date is too much in the future, '
                                 f'or incorrect datetime specified, for example hour=24')
            elif r.status_code == 500:
                logging.critical(f'{f_name}-request failed probably due to many requests in too short a time')

            try:
                logging.critical(f'JSON is {json.dumps(r.json(), indent=4)}')
            except ValueError:
                pass
        else:
            logging.debug(f'{f_name}-request successful')

    def _xml_content_to_json(self, response: requests.Response) -> Dict:
        # TODO exception handling
        response_content = html.unescape(response.content.decode('utf-8'))
        response_json = self._xml_str_to_json(response_content)

        return response_json

    def _set_headers(self):
        self.headers_json = {'Accept': 'application/json',
                             'Authorization': 'Bearer ' + self.access_token}
        self.headers_xml = {'Accept': 'application/xml',
                            'Authorization': 'Bearer ' + self.access_token}

    def _get_url(self, url_part: str, suffix=()) -> str:
        if type(suffix) is str:
            return self.urls['base'] + url_part + suffix
        else:
            return self.urls['base'] + url_part + '/'.join(suffix)

    @staticmethod
    def _decode_xml_content(response: requests.Response) -> str:
        try:
            response_content = html.unescape(response.content.decode('utf-8'))
        except Exception as e:
            logging.critical(f'Could not decode xml content; error_msg: {str(e)}')
            response_content = None

        return response_content

    @staticmethod
    def _xml_str_to_json(xml_str: str) -> Dict:
        try:
            json_dict = xmltodict.parse(xml_str)
        except xml.parsers.expat.ExpatError as e:
            logging.critical(f'Parsing of xml-response not possible; xml_str: {str}; error_msg: {str(e)}')
            json_dict = None

        return json_dict
