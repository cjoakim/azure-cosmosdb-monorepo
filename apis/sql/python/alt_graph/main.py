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
    parse_azure_rbac_roles_html()
    parse_azure_ad_rbac_permissions_roles_html()

def parse_azure_rbac_roles_html():
    print('parse_azure_rbac_roles_html')
    html = FS.read('data/rbac/azure_roles.html')
    print('roles_html length: {}'.format(len(html)))
    roles_list = list()

    # <table id="all_table">    <-- I added the id on line 546, after <h2 id="all">All</h2>
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

    soup = BeautifulSoup(html, "html.parser")
    all_table = soup.find(id='all_table')
    rows = all_table.find_all('tr')
    for tr_idx, tr in enumerate(rows):
        tds = tr.find_all('td')
        if len(tds) == 3:
            role, href, desc, id = '', '', '', ''
            print('--- {}'.format(tr_idx))
            print('tr: {}'.format(tr))
            td1 = tds[0]
            td2 = tds[1]
            td3 = tds[2]
            try:
                role = td1.text
                link = td1.find_all('a', href=True)[0]
                href = link['href'].replace('#','')
                desc = td2.text
                id   = td3.text.strip()

                if len(id) > 0:
                    obj = dict()
                    obj['role'] = role
                    obj['href'] = href
                    obj['desc'] = desc
                    obj['id']   = id
                    print(json.dumps(obj, indent=2, sort_keys=False))
                    roles_list.append(obj)
            except:
                print('ERROR: unable to parse row {} {}'.format(tr_idx, tr))


    print('parsed roles count: {}'.format(len(roles_list)))
    FS.write_json(roles_list, 'data/rbac/azure_roles.json')

def parse_azure_ad_rbac_permissions_roles_html():
    print('parse_azure_ad_rbac_permissions_roles_html')
    html = FS.read('data/rbac/azure_ad_roles_permissions.html')
    print('perms_html length: {}'.format(len(html)))
    objects_list = list()

    soup = BeautifulSoup(html, "html.parser")

    # First, capture all of the H2 tag titles for reference
    h2_title_list = list()
    for h2 in soup.find_all('h2'):
        h2_title_list.append(h2.text)
    FS.write_json(h2_title_list, 'tmp/azure_ad_roles_permissions_h2_title_list.json')

    # Next, iterate all the tables, and find_previous their h2 title
    tables = soup.find_all('table')

    for table_idx, table in enumerate(tables):
        h2 = table.find_previous('h2')
        h2_title = h2.text
        print('=== {} {}'.format(table_idx, h2_title))

        for tr_idx, tr in enumerate(table):
            tbody = table.find_next('tbody')
            if h2_title == 'All roles':
                rows = tbody.find_all('tr')
                for tr_idx, tr in enumerate(rows):
                    try:
                        tds = tr.find_all('td')
                        if len(tds) == 3:
                            print(tr)
                            # <tr>
                            # <td><a data-linktype="self-bookmark" href="#application-administrator">Application Administrator</a></td>
                            # <td>Can create and manage all aspects of app registrations and enterprise apps.</td>
                            # <td>9b895d92-2cd3-44c7-9d02-a6ac2d5ea5c3</td>
                            # </tr>
                            td1 = tds[0]
                            td2 = tds[1]
                            td3 = tds[2]
                            link = td1.find_all('a', href=True)[0]
                            href = link['href'].replace('#','')
                            obj = dict()
                            obj['cat']  = h2_title
                            obj['type'] = 'role'
                            obj['role'] = td1.text
                            obj['href'] = href
                            obj['desc'] = td2.text
                            obj['id']   = td3.text
                            print(json.dumps(obj, indent=2, sort_keys=False))
                            objects_list.append(obj)
                    except:
                        print('ERROR: unable to parse row {} in {}'.format(tr_idx, h2_title))    
            else:
                if ignore_this_section(h2_title):
                    pass
                else:
                    rows = tbody.find_all('tr')
                    for tr_idx, tr in enumerate(rows):
                        try:
                            tds = tr.find_all('td')
                            if len(tds) == 2:
                                print(tr)
                                td1 = tds[0]
                                td2 = tds[1]
                                obj = dict()
                                obj['cat']  = h2_title
                                obj['type'] = 'permission'
                                obj['actions'] = tds[0].text
                                obj['desc'] = tds[1].text
                                print(json.dumps(obj, indent=2, sort_keys=False))
                                objects_list.append(obj) 
                        except:
                            print('ERROR: unable to parse row {} in {}'.format(tr_idx, h2_title))   
    print('parsed permissions count: {}'.format(len(objects_list)))
    FS.write_json(objects_list, 'data/rbac/azure_ad_roles_permissions.json')

def ignore_this_section(h2_title):
    if h2_title == "How to understand role permissions":
        return True
    if h2_title == "Deprecated roles":
        return True
    if h2_title == "Roles not shown in the portal":
        return True
    if h2_title == "Password reset permissions":
        return True
    if h2_title == "Next steps":
        return True
    if h2_title == "Feedback":
        return True
    return False


if __name__ == "__main__":
    func = sys.argv[1].lower()

    if func == 'parse_azure_rbac_docs_html':
        parse_azure_rbac_docs_html()
    elif func == 'xxx':
        pass
    else:
        print_options('Error: invalid function: {}'.format(func))
