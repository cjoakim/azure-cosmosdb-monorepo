"""
Usage:
  python main.py <func> <args...>
  python main.py parse_azure_rbac_docs_html
Options:
  -h --help     Show this screen.
  --version     Show version.
"""

__author__  = 'Chris Joakim'
__email__   = "chjoakim@microsoft.com"
__license__ = "MIT"
__version__ = "2022/06/24"

import json
import sys
import time
import os

import arrow 

from docopt import docopt

from pysrc.bytes import Bytes 
from pysrc.cosmos import Cosmos
from pysrc.env import Env
from pysrc.fs import FS
from pysrc.rcache import RCache

GENERATED_APP_RBAC_DATA_JSON = 'data/rbac/generated_application_rbac_data.json'


def print_options(msg):
    print(msg)
    arguments = docopt(__doc__, version=__version__)
    print(arguments)

def load_cosmos():
    app_data = FS.read_json(GENERATED_APP_RBAC_DATA_JSON)
    print('load_cosmos')
    print(app_data)

def query_cosmos():
    print('query_cosmos')


if __name__ == "__main__":
    func = sys.argv[1].lower()

    if func == 'load_cosmos':
        load_cosmos()
    elif func == 'xxx':
        query_cosmos()
    else:
        print_options('Error: invalid function: {}'.format(func))
