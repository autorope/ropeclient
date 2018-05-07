
"""
Functions that specify how to access api.
"""

import calendar
import requests
import time
import datetime
import json

# from six.moves.urllib.request import pathname2url

from six.moves.urllib import parse

from . import error, util


def _encode_datetime(dttime):
    if dttime.tzinfo and dttime.tzinfo.utcoffset(dttime) is not None:
        utc_timestamp = calendar.timegm(dttime.utctimetuple())
    else:
        utc_timestamp = time.mktime(dttime.timetuple())

    return int(utc_timestamp)


def _api_encode(data):
    for key, value in data.items():
        if value is None:
            continue
        elif isinstance(value, datetime.datetime):
            yield (key, _encode_datetime(value))
        else:
            yield (key, value)


def _build_api_url(url, query):
    scheme, netloc, path, base_query, fragment = parse.urlsplit(url)
    if base_query:
        query = str('%s&%s' % (base_query, query))

    return parse.urlunsplit((scheme, netloc, path, query, fragment))


class APIRequester(object):

    def __init__(self, auth_token=None):
        self.auth_token = auth_token
        self.params = {'format': 'json'}

    def _build_headers(self, auth_token, headers={}):
        if self.auth_token:
            my_auth_token = self.auth_token
        else:
            from . import auth_token
            my_auth_token = auth_token

        auth_header = {'Authorization': 'Token {}'.format(my_auth_token)}
        headers.update(auth_header)
        return headers

    def get_api_base(self, ):
        from . import api_base
        return api_base

    def get_request(self, url, params={}, supplied_headers={}, format='json'):

        # combine default params and given params
        params_all = {}
        params_all.update(self.params)
        params_all.update(params)

        abs_url = self.get_api_base() + url
        encoded_params = parse.urlencode(list(_api_encode(params_all)))
        abs_url = _build_api_url(abs_url, encoded_params)

        # print('abs_url: {}'.format(abs_url))
        headers = self._build_headers(self.auth_token, supplied_headers)

        resp = requests.get(abs_url, headers=headers)
        if format == 'json':
            return self.get_safe_json_response(resp)
        elif format == 'text':
            return resp.text
        elif format == 'gdf':
            import tempfile
            import geopandas as gp
            file = tempfile.NamedTemporaryFile(suffix='.json', delete=False, mode='w')
            file.write(resp.text)
            file.close()

            gdf = gp.read_file(file.name)
            return gdf

    def post_request(self, url, data, params=None, supplied_headers={}, files=None):
        abs_url = self.get_api_base() + url

        encoded_params = parse.urlencode(list(_api_encode(params or {})))
        abs_url = _build_api_url(abs_url, encoded_params)
        headers = self._build_headers(self.auth_token, supplied_headers)
        resp = requests.post(abs_url, json=data, headers=headers, files=files)
        return self.get_safe_json_response(resp)

    def post_file_request(self, url, files, data=None, params=None, supplied_headers={}, ):
        abs_url = self.get_api_base() + url

        encoded_params = parse.urlencode(list(_api_encode(params or {})))
        abs_url = _build_api_url(abs_url, encoded_params)
        headers = self._build_headers(self.auth_token, supplied_headers)
        resp = requests.post(abs_url, headers=headers, data=data, files=files)
        return self.get_safe_json_response(resp)

    def patch_request(self, url, data, params=None, supplied_headers={}, files=None):
        abs_url = self.get_api_base() + url

        encoded_params = parse.urlencode(list(_api_encode(params or {})))
        abs_url = _build_api_url(abs_url, encoded_params)
        headers = self._build_headers(self.auth_token, supplied_headers)
        resp = requests.patch(abs_url, json=data, headers=headers, files=files)
        return self.get_safe_json_response(resp)

    def get_safe_json_response(self, response):
        """
        Get the response safely and show errors if it fails.
        """
        try:
            json_data = response.json()
        except json.JSONDecodeError as e:
            try:
                if response.status_code == 404:
                    print('404 error, check your url. {}'.format(response.url))
                else:
                    print('status_code: {}'.format(response.status_code))
            except:
                pass
            print('JSON decoding error.')
            print('response text:')
            print(response.text)
            print(e)
            return None

        return json_data

    def handle_error_response(self, rbody, rcode, resp, rheaders):
        try:
            error_data = resp['error']
        except (KeyError, TypeError):
            raise error.APIError(
                "Invalid response object from API: %r (HTTP response code "
                "was %d)" % (rbody, rcode),
                rbody, rcode, resp)

    def interpret_response(self, rbody, rcode, rheaders):
        try:
            if hasattr(rbody, 'decode'):
                rbody = rbody.decode('utf-8')
            resp = util.json.loads(rbody)
        except Exception:
            raise error.APIError(
                "Invalid response body from API: %s "
                "(HTTP response code was %d)" % (rbody, rcode),
                rbody, rcode, rheaders)
        if not (200 <= rcode < 300):
            self.handle_error_response(rbody, rcode, resp, rheaders)
        return resp
