__version__ = '0.0.0'

auth_token = None
api_base = 'http://localhost:8000'

from . import resource

Bot = resource.Bot()
Record = resource.Record()
Net = resource.Net()


import os
CODE_PATH = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(os.path.dirname(CODE_PATH), 'data')


"""
CONFIG
"""
from six.moves import configparser
config_dir = os.path.expanduser('~/.rope')
config_file = os.path.join(config_dir, 'settings.ini')
config = configparser.ConfigParser()

try:
    config.read(config_file)
    auth_token = config['credentials']['token']
except:
    print("Couldn't find {} file.".format(config_file))