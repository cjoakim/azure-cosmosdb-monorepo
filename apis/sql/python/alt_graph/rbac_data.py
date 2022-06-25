"""
Usage:
  python rbac_data.py <func> <args...>
  python rbac_data.py parse_azure_rbac_docs_html
  python rbac_data.py generate_cosmosdb_datasets 1000
Options:
  -h --help     Show this screen.
  --version     Show version.
"""

# Chris Joakim, Microsoft, June 2022

import json
import sys
import random
import time
import os

import arrow 

from bs4 import BeautifulSoup
from docopt import docopt
from faker import Faker

from pysrc.bytes import Bytes 
from pysrc.cosmos import Cosmos
from pysrc.env import Env
from pysrc.fs import FS
from pysrc.rcache import RCache

PARSED_AZURE_ROLES_JSON          = 'data/rbac/azure_roles.json'
PARSED_AD_ROLES_PERMISSIONS_JSON = 'data/rbac/azure_ad_roles_permissions.json'
GENERATED_APP_RBAC_DATA_JSON     = 'data/rbac/generated_application_rbac_data.json'

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
    FS.write_json(roles_list, PARSED_AZURE_ROLES_JSON)

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
    FS.write_json(objects_list, PARSED_AD_ROLES_PERMISSIONS_JSON)

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

def generate_cosmosdb_datasets(app_count):
    print('generate_cosmosdb_datasets')
    azure_roles_data = FS.read_json(PARSED_AZURE_ROLES_JSON)
    print('loaded {}, count: {}'.format(PARSED_AZURE_ROLES_JSON, len(azure_roles_data)))
    azure_ad_data = FS.read_json(PARSED_AD_ROLES_PERMISSIONS_JSON)
    print('loaded {}, count: {}'.format(PARSED_AD_ROLES_PERMISSIONS_JSON, len(azure_ad_data)))
    azure_ad_roles = list()
    for obj in azure_ad_data:
        if obj['type'] == 'role':
            azure_ad_roles.append(obj)

    # generate n-number of "applications" - with fake name
    # app -> has roles
    #   role xxx-owners = a list of 1-3 human Owners  (xxx = app name)
    #   role xxx-administrators = a list of 1-3 human Application Administrator  (xxx = app name)
    #   role xxx-contributors = a list of 1-12 humans
    #                           include the role "Contributor"  (azure_roles file)
    #                           include the role "Application Developer" (azure_ad_roles_permissions)
    #                           include 0-5 random roles (azure_ad_roles_permissions)
    #   role xxx-writer-apps  = a list of 0-3 writer apps
    #   role xxx-reader-apps  = a list of 1-10 writer apps
    # user -> has roles  (a list of the roles they have in the scope of each app)

    owner_names, developer_names = generate_random_human_names(app_count)
    people_list = generate_people_list(owner_names, developer_names)

    apps_list = generate_random_apps(app_count)
    for app_idx, app in enumerate(apps_list):
        assign_app_owners(app, app_idx, owner_names)
        assign_app_administrators(app, app_idx, developer_names)
        assign_app_contributors(app, app_idx, developer_names)

    for app_idx, app in enumerate(apps_list):
        augment_app_owners(app, app_idx, azure_roles_data, azure_ad_roles)
        augment_app_administrators(app, app_idx, azure_roles_data, azure_ad_roles)
        augment_app_contributors(app, app_idx, azure_roles_data, azure_ad_roles)

    # create one aggregate data structure for all data needs for this sample app
    agg_data = dict()
    agg_data['apps'] = apps_list
    agg_data['people'] = people_list
    agg_data['azure_roles_data'] = azure_roles_data
    agg_data['azure_ad_data'] = azure_ad_data
    FS.write_json(agg_data, GENERATED_APP_RBAC_DATA_JSON)

def generate_random_apps(app_count):
    app_names, apps = list(), list()
    for n in range(app_count):
        app_names.append('app{}'.format(n + 1))
    for app_name in app_names:
        app = dict()
        app['name'] = app_name
        app['writers_apps'] = random_app_names(app_name, app_names, 0, 3)
        app['reader_apps']  = random_app_names(app_name, app_names, 0, 10)
        apps.append(app)
    return apps

def random_app_names(app_name, names_list, min_count, max_count):
    names = dict()
    count = random.randint(min_count, max_count)
    for n in range(count):
        ridx = random.randint(0, len(names_list) - 1)
        rname = names_list[ridx]
        if rname != app_name:
            names[rname] = ridx
    return sorted(names.keys())

def generate_random_human_names(count):
    owner_names, developer_names = dict(), dict()
    owner_count = count 
    developer_count = count * 10
    faker = Faker()
    while len(owner_names) < owner_count:
        name = faker.name()
        owner_names[name] = ''
        if random.randint(0, 10) < 3:
            developer_names[name] = ''
    while len(developer_names) < developer_count:
        name = faker.name()
        developer_names[name] = ''
    return (sorted(owner_names.keys()), sorted(developer_names.keys()))

def generate_people_list(owner_names, developer_names):
    names, people = list(), list()
    faker = Faker()
    for name in owner_names:
        names.append(name)
    for name in developer_names:
        names.append(name)

    for name_idx, name in enumerate(names):
        person = dict()
        person['name'] = name
        person['empl_id'] = name_idx + 1
        person['hire_date'] = faker.date()
        person['city']      = faker.city()
        person['state']     = faker.state()
        people.append(person)

    return people

def assign_app_owners(app, app_idx, owner_names):
    person = dict()
    person['name'] = owner_names[app_idx]
    app['owners'] = [person]

def assign_app_administrators(app, app_idx, developer_names):
    count = random.randint(1, 3)
    administrators = dict()
    while len(administrators.keys()) < count:
        ridx  = random.randint(0, len(developer_names) - 1)
        rname = developer_names[ridx]
        person = dict()
        person['name'] = rname
        administrators[rname] = person
    app['administrators'] = list()
    for name in sorted(administrators.keys()):
        person = administrators[name]
        app['administrators'].append(person)

def assign_app_contributors(app, app_idx, developer_names):
    count = random.randint(1, 12)
    contributors = dict()
    while len(contributors.keys()) < count:
        ridx  = random.randint(0, len(developer_names) - 1)
        rname = developer_names[ridx]
        person = dict()
        person['name'] = rname
        contributors[rname] = person
    app['contributors'] = list()
    for name in sorted(contributors.keys()):
        person = contributors[name]
        app['contributors'].append(person)

def augment_app_owners(app, app_idx, azure_roles_data, azure_ad_roles):
    for person in app['owners']:
        role_name = 'app_{}_owner'.format(app['name'])
        person['roles'] = list()
        person['roles'].append(role_name)
        for n in range(random.randint(0, 3)):
            ridx = random.randint(0, len(azure_roles_data) - 1)
            role = azure_roles_data[ridx]
            person['roles'].append(role['role'])
        for n in range(random.randint(0, 3)):
            ridx = random.randint(0, len(azure_ad_roles) - 1)
            role = azure_ad_roles[ridx]
            person['roles'].append(role['role'])


def augment_app_administrators(app, app_idx, azure_roles_data, azure_ad_roles):
    for person in app['administrators']:
        role_name = 'app_{}_administrator'.format(app['name'])
        person['roles'] = list()
        person['roles'].append(role_name)
        for n in range(random.randint(0, 3)):
            ridx = random.randint(0, len(azure_roles_data) - 1)
            role = azure_roles_data[ridx]
            person['roles'].append(role['role'])
        for n in range(random.randint(2, 6)):
            ridx = random.randint(0, len(azure_ad_roles) - 1)
            role = azure_ad_roles[ridx]
            person['roles'].append(role['role'])


def augment_app_contributors(app, app_idx, azure_roles_data, azure_ad_roles):
    for person in app['contributors']:
        role_name = 'app_{}_contributor'.format(app['name'])
        person['roles'] = list()
        person['roles'].append(role_name)
        for n in range(random.randint(0, 3)):
            ridx = random.randint(0, len(azure_roles_data) - 1)
            role = azure_roles_data[ridx]
            person['roles'].append(role['role'])
        for n in range(random.randint(3, 12)):
            ridx = random.randint(0, len(azure_ad_roles) - 1)
            role = azure_ad_roles[ridx]
            person['roles'].append(role['role'])


if __name__ == "__main__":
    func = sys.argv[1].lower()

    if func == 'parse_azure_rbac_docs_html':
        parse_azure_rbac_docs_html()
    elif func == 'generate_cosmosdb_datasets':
        app_count = int(sys.argv[2])
        generate_cosmosdb_datasets(app_count)
    else:
        print_options('Error: invalid function: {}'.format(func))
