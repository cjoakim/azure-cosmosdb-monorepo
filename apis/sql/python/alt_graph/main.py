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

from bs4 import BeautifulSoup
from docopt import docopt

from pysrc.bytes import Bytes 
from pysrc.cosmos import Cosmos
from pysrc.env import Env
from pysrc.fs import FS
from pysrc.rcache import RCache


def print_options(msg):
    print(msg)
    arguments = docopt(__doc__, version=__version__)
    print(arguments)

def parse_azure_rbac_docs_html():
    print('parse_azure_rbac_docs_html')
    roles_html = FS.read('data/rbac/roles.html')
    perms_html = FS.read('data/rbac/permissions.html')
    print('roles_html length: {}'.format(len(roles_html)))
    print('perms_html length: {}'.format(len(perms_html)))
    roles_list = list()
    perms_list = list()

    soup = BeautifulSoup(roles_html, "html.parser")
    # <table id="all_table">    <-- I added the id on line 546 after <h2 id="all">All</h2>

    # Example html and parsed output:
    # tr: <tr>
    # <td><a data-linktype="self-bookmark" href="#scheduler-job-collections-contributor">Scheduler Job Collections Contributor</a></td>
    # <td>Lets you manage Scheduler job collections, but not access to them.</td>
    # <td>188a0f2f-5c9e-469b-ae67-2aa5ce574b94</td>
    # </tr>
    # {
    #   "role": "Scheduler Job Collections Contributor",
    #   "href": "scheduler-job-collections-contributor",
    #   "desc": "Lets you manage Scheduler job collections, but not access to them.",
    #   "id": "188a0f2f-5c9e-469b-ae67-2aa5ce574b94"
    # }

    all_table = soup.find(id='all_table')
    rows = all_table.find_all('tr')
    for tr_idx, tr in enumerate(rows):
        tds = tr.find_all('td')
        if len(tds) == 3:
            role, href, desc, id = '', '', '', ''
            print('---')
            print('tr: {}'.format(tr))
            td1 = tds[0]
            td2 = tds[1]
            td3 = tds[2]
            try:
                role = td1.text
                link = td1.find_all('a', href=True)[0]
                href = link['href'].replace('#','')
                desc = td2.text
                id   = td3.text
            except:
                print('unable to parse row {} {}'.format(tr_idx, tr))
            obj = dict()
            obj['role'] = role
            obj['href'] = href
            obj['desc'] = desc
            obj['id']   = id
            print(json.dumps(obj, indent=2, sort_keys=False))
            roles_list.append(obj)
    print('parsed roles count: {}'.format(len(roles_list)))
    FS.write_json(roles_list, 'data/rbac/roles.json')


if __name__ == "__main__":
    func = sys.argv[1].lower()

    if func == 'parse_azure_rbac_docs_html':
        parse_azure_rbac_docs_html()
    elif func == 'xxx':
        pass
    else:
        print_options('Error: invalid function: {}'.format(func))
