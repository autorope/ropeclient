"""
Access to autorope api.
"""
import os

from ropeclient import auth_token
from ropeclient.api_requestor import APIRequester
import json

import requests


class BaseResource(APIRequester):
    def __init__(self):
        super(BaseResource, self).__init__()

    def list(self):
        pilot_text = self.get_request(self.url, format='text')
        pilot_json = json.loads(pilot_text)
        return pilot_json

    def retrieve(self, id, format='json'):
        url = self.url + '{}/'.format(id)
        params = {'format': 'json'}
        resp_json = self.get_request(url, params, format=format)
        return resp_json


class Bot(BaseResource):
    url = '/api/bots/'


class Record(BaseResource):
    url = '/api/records/'

    def create(self, data=None, files=None):
        """
        crop_id 38 is None
        """
        resp = self.post_file_request(self.url, data=data, files=files)
        return resp

class Net(BaseResource):
    url = '/api/records/'