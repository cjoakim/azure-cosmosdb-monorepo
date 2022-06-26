"""
Usage:
  python main.py <func> <args...>
  python main.py parse_azure_rbac_docs_html
  python main.py generate_application_data 1000
  python main.py generate_cosmosdb_load_files
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
import uuid

import arrow 

from bs4 import BeautifulSoup
from docopt import docopt
from faker import Faker

from pysrc.bytes import Bytes 
from pysrc.cosmos import Cosmos
from pysrc.env import Env
from pysrc.fs import FS
from pysrc.rcache import RCache

PARSED_AZURE_ROLES_JSON          = 'data/raw/azure_roles.json'
PARSED_AD_ROLES_PERMISSIONS_JSON = 'data/raw/azure_ad_roles_permissions.json'
GENERATED_APP_RBAC_DATA_JSON     = 'data/raw/generated_application_rbac_data.json'

COSMOSDB_ID_ATTR                 = 'id'
COSMOSDB_PK_ATTR                 = 'pk'
COSMOSDB_DOCTYPE_ATTR            = 'doctype'

APP_COUNT = 0;
APPS_MAP                 = dict()
PEOPLE_MAP               = dict()
AZURE_ROLES_MAP          = dict()
AZURE_AD_ROLES_MAP       = dict()
AZURE_AD_PERMISSIONS_MAP = dict()
AZURE_APP_ROLES_MAP      = dict()

def print_options(msg):
    print(msg)
    arguments = docopt(__doc__, version='1.0.0')
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

def generate_application_data(app_count):
    print('generate_application_data')
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
    agg_data['app_count'] = app_count
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

def generate_cosmosdb_load_files():
    print('generate_cosmosdb_load_files')
    app_data = FS.read_json(GENERATED_APP_RBAC_DATA_JSON)
    print(sorted(app_data.keys())) # ['apps', 'azure_ad_data', 'azure_roles_data', 'people']

    generate_application_roles(app_data)
    generate_cosmosdb_azure_roles_load_file(app_data)
    generate_cosmosdb_azure_ad_load_files(app_data)
    generate_cosmosdb_people_load_file(app_data)
    generate_cosmosdb_apps_load_file(app_data)
    generate_cosmosdb_edges_load_file(app_data)

    FS.write_json(APPS_MAP,                 'data/load/apps_map.json')
    FS.write_json(PEOPLE_MAP,               'data/load/people_map.json')
    FS.write_json(AZURE_ROLES_MAP,          'data/load/azure_roles_map.json')
    FS.write_json(AZURE_AD_ROLES_MAP,       'data/load/azure_ad_roles_map.json')
    FS.write_json(AZURE_AD_PERMISSIONS_MAP, 'data/load/azure_ad_permissions_map.json')

def generate_application_roles(app_data):
    app_roles = app_data['app_roles']
    application_role_lines = list()
    for app_role in app_roles:
        doc = id_map('application_role')
        doc[COSMOSDB_PK_ATTR] = app_role
        doc['name'] = app_role
        application_role_lines.append(json.dumps(doc) + os.linesep)
        AZURE_APP_ROLES_MAP[app_role] = doc[COSMOSDB_PK_ATTR]
    FS.write_lines(application_role_lines, 'data/load/application_roles.json')

def generate_cosmosdb_azure_roles_load_file(app_data):
    objects = app_data['azure_roles_data']
    azure_role_lines = list()
    for obj in objects:
        doc = id_map('azure_role')
        doc[COSMOSDB_PK_ATTR] = obj['role']
        doc.update(obj)
        role = doc['role']
        AZURE_ROLES_MAP[role] = doc[COSMOSDB_ID_ATTR]
        azure_role_lines.append(json.dumps(doc) + os.linesep)

    FS.write_lines(azure_role_lines, 'data/load/azure_roles.json')

def generate_cosmosdb_azure_ad_load_files(app_data):
    objects = app_data['azure_ad_data']
    ad_role_lines, ad_perm_lines = list(), list()

    # roles
    for obj in objects:
        obj_type = obj['type']
        if obj_type == 'role':
            del obj['id']
            doc = id_map('ad_role')
            doc[COSMOSDB_PK_ATTR] = obj['role']
            doc.update(obj)
            role = doc['role']
            AZURE_AD_ROLES_MAP[role] = doc[COSMOSDB_ID_ATTR]
            ad_role_lines.append(json.dumps(doc) + os.linesep)

    # permissions
    for obj in objects:
        obj_type = obj['type']
        if obj_type == 'permission':
            category = obj['cat']
            doc = id_map('ad_permission')
            doc[COSMOSDB_PK_ATTR] = category
            doc.update(obj)
            #doc['cat_id'] = AZURE_AD_ROLES_MAP[category]
            actions = doc['actions']
            AZURE_AD_PERMISSIONS_MAP[actions] = doc[COSMOSDB_ID_ATTR]
            ad_perm_lines.append(json.dumps(doc) + os.linesep)

    FS.write_lines(ad_role_lines, 'data/load/azure_ad_roles.json')
    FS.write_lines(ad_perm_lines, 'data/load/azure_ad_permissions.json')

def generate_cosmosdb_people_load_file(app_data):
    objects = app_data['people']
    people_lines = list()
    for obj in objects:
        doc = id_map('person')
        doc[COSMOSDB_PK_ATTR] = obj['name']
        doc.update(obj)
        name = doc['name']
        PEOPLE_MAP[name] = doc[COSMOSDB_ID_ATTR]
        people_lines.append(json.dumps(doc) + os.linesep)

    FS.write_lines(people_lines, 'data/load/people.json')

def generate_cosmosdb_apps_load_file(app_data):
    objects = app_data['apps']
    app_lines = list()
    for obj in objects:
        doc = id_map('app')
        name = obj['name']
        doc[COSMOSDB_PK_ATTR] = name
        doc.update(obj)
        APPS_MAP[name] = doc[COSMOSDB_ID_ATTR]
        app_lines.append(json.dumps(doc) + os.linesep)

    FS.write_lines(app_lines, 'data/load/apps.json')

def generate_cosmosdb_edges_load_file(app_data):
    print('generate_cosmosdb_edges_load_file')
    edge_lines = list()
    generate_edges_apps_and_apps(app_data, edge_lines)
    generate_edges_apps_and_people(app_data, edge_lines)
    generate_edges_ad_roles_permissions(app_data, edge_lines)
    generate_edges_people_roles(app_data, edge_lines)

    FS.write_lines(edge_lines, 'data/load/edges.json')

def generate_edges_apps_and_apps(app_data, edge_lines):
    apps = app_data['apps']
    for app in apps:
        app_name = app['name']

        for subject_app in app['reader_apps']:
            edge = empty_edge_doc()
            edge['subject'] = app_name
            edge['subject_doctype'] = 'app'
            edge['subject_id'] = APPS_MAP[app_name]
            edge['subject_pk'] = app_name
            edge['predicate'] = 'reader'
            edge['object'] = subject_app
            edge['object_doctype'] = 'app'
            edge['object_id'] = APPS_MAP[subject_app]
            edge['object_pk'] = subject_app
            edge_lines.append(json.dumps(edge) + os.linesep)

            iedge = inverse_edge(edge, 'read_by')
            edge_lines.append(json.dumps(iedge) + os.linesep)

        for subject_app in app['writer_apps']:
            edge = empty_edge_doc()
            edge['subject'] = app_name
            edge['subject_doctype'] = 'app'
            edge['subject_id'] = APPS_MAP[app_name]
            edge['subject_pk'] = app_name
            edge['predicate'] = 'writer'
            edge['object'] = subject_app
            edge['object_doctype'] = 'app'
            edge['object_id'] = APPS_MAP[subject_app]
            edge['object_pk'] = subject_app
            edge_lines.append(json.dumps(edge) + os.linesep)
            
            iedge = inverse_edge(edge, 'written_by')
            edge_lines.append(json.dumps(iedge) + os.linesep)

def generate_edges_apps_and_people(app_data, edge_lines):
    apps = app_data['apps']
    for app in apps:
        app_name = app['name']
        for person in app['owners']:
            person_name = person['name']
            edge = empty_edge_doc()
            edge['subject'] = app_name
            edge['subject_doctype'] = 'app'
            edge['subject_id'] = APPS_MAP[app_name]
            edge['subject_pk'] = app_name
            edge['predicate'] = 'owned_by'
            edge['object'] = person_name
            edge['object_doctype'] = 'person'
            edge['object_id'] = PEOPLE_MAP[person_name]
            edge['object_pk'] = person_name
            edge_lines.append(json.dumps(edge) + os.linesep)

            iedge = inverse_edge(edge, 'owns')
            edge_lines.append(json.dumps(iedge) + os.linesep)

        for person in app['administrators']:
            person_name = person['name']
            edge = empty_edge_doc()
            edge['subject'] = app_name
            edge['subject_doctype'] = 'app'
            edge['subject_id'] = APPS_MAP[app_name]
            edge['subject_pk'] = app_name
            edge['predicate'] = 'administered_by'
            edge['object'] = person_name
            edge['object_doctype'] = 'person'
            edge['object_id'] = PEOPLE_MAP[person_name]
            edge['object_pk'] = person_name
            edge_lines.append(json.dumps(edge) + os.linesep)

            iedge = inverse_edge(edge, 'administers')
            edge_lines.append(json.dumps(iedge) + os.linesep)

        for person in app['contributors']:
            person_name = person['name']
            edge = empty_edge_doc()
            edge['subject'] = app_name
            edge['subject_doctype'] = 'app'
            edge['subject_id'] = APPS_MAP[app_name]
            edge['subject_pk'] = app_name
            edge['predicate'] = 'contributor_by'
            edge['object'] = person_name
            edge['object_doctype'] = 'person'
            edge['object_id'] = PEOPLE_MAP[person_name]
            edge['object_pk'] = person_name
            edge_lines.append(json.dumps(edge) + os.linesep)

            iedge = inverse_edge(edge, 'contributes_to')
            edge_lines.append(json.dumps(iedge) + os.linesep)

def generate_edges_ad_roles_permissions(app_data, edge_lines):
    ad_data = app_data['azure_ad_data']
    for data in ad_data:
        data_type = data['type']
        if data_type == 'permission':
            role_name = data['cat']
            actions   = data['actions']

            edge = empty_edge_doc()
            edge['subject'] = role_name
            edge['subject_doctype'] = 'ad_role'
            edge['subject_id'] = AZURE_AD_ROLES_MAP[role_name]
            edge['subject_pk'] = role_name
            edge['predicate'] = 'contains_ad_permission'
            edge['object']    = actions
            edge['object_doctype'] = 'ad_permission'
            edge['object_id'] = AZURE_AD_PERMISSIONS_MAP[actions]
            edge['object_pk'] = role_name
            edge_lines.append(json.dumps(edge) + os.linesep)

            iedge = inverse_edge(edge, 'in_ad_role')
            edge_lines.append(json.dumps(iedge) + os.linesep)

def generate_edges_people_roles(app_data, edge_lines):
    apps = app_data['apps']
    for app in apps:
        app_name = app['name']
        for app_role_type in 'owners,administrators,contributors'.split(','):
            for person_obj in app[app_role_type]:
                person_name = person_obj['name']
                person_roles = person_obj['roles']
                for person_role in person_roles:
                    id, role_type = lookup_role_id(person_role)

                    edge = empty_edge_doc()
                    edge['subject'] = person_name
                    edge['subject_doctype'] = 'person'
                    edge['subject_id'] = id
                    edge['subject_pk'] = person_role
                    edge['predicate'] = 'has_role'
                    edge['object']    = app_name
                    edge['object_doctype'] = 'app'
                    edge['object_id'] = APPS_MAP[app_name]
                    edge['object_pk'] = app_name
                    edge_lines.append(json.dumps(edge) + os.linesep)

                    iedge = inverse_edge(edge, 'has_person')
                    edge_lines.append(json.dumps(iedge) + os.linesep)

def lookup_role_id(role_name):
    if role_name in AZURE_APP_ROLES_MAP.keys():
        return (AZURE_APP_ROLES_MAP[role_name], 'application_role')
    if role_name in AZURE_ROLES_MAP.keys():
        return (AZURE_ROLES_MAP[role_name], 'azure_role')
    if role_name in AZURE_AD_ROLES_MAP.keys():
        return (AZURE_AD_ROLES_MAP[role_name], 'ad_role')
    return ('','undefined_role')

def empty_edge_doc():
    # stub-out the edge, caller to populate these attributes
    doc = id_map('edge')
    doc['subject'] = ''
    doc['subject_doctype'] = ''
    doc['subject_id'] = ''
    doc['subject_pk'] = ''
    doc['predicate'] = ''
    doc['object'] = ''
    doc['object_doctype'] = ''
    doc['object_id'] = ''
    doc['object_pk'] = ''
    return doc

def inverse_edge(edge, predicate):
    doc = empty_edge_doc()
    doc['subject']         = edge['object']
    doc['subject_doctype'] = edge['object_doctype']
    doc['subject_id']      = edge['object_id']
    doc['subject_pk']      = edge['object_pk']
    doc['predicate']       = predicate
    doc['object']          = edge['subject']
    doc['object_doctype']  = edge['subject_doctype']
    doc['object_id']       = edge['subject_id']
    doc['object_pk']       = edge['subject_pk']
    return doc

def id_map(doctype):
    map = dict()
    map[COSMOSDB_ID_ATTR] = str(uuid.uuid4())
    map[COSMOSDB_DOCTYPE_ATTR] = doctype
    return map

def scan_generated_cosmosdb_load_files():
    print('scan_generated_cosmosdb_load_files')
    files = FS.walk('data/load')
    file_count, total_lines_count = 0, 0
    for file in files:
        path = file['full']
        if path.endswith('.json'):
            file_count = file_count + 1
            file_lines = FS.read_lines(path)
            file_line_count = len(file_lines)
            total_lines_count = total_lines_count + file_line_count
            print('{} lines in file {}'.format(file_line_count, path))
    print('{} total lines in {} json files'.format(total_lines_count, file_count))


if __name__ == "__main__":

    print(sys.argv)

    if len(sys.argv) > 1:
        func = sys.argv[1].lower()

        if func == 'parse_azure_rbac_docs_html':
            parse_azure_rbac_docs_html()

        elif func == 'generate_application_data':
            app_count = int(sys.argv[2])
            generate_application_data(app_count)

        elif func == 'generate_cosmosdb_load_files':
            generate_cosmosdb_load_files()

        elif func == 'scan_generated_cosmosdb_load_files':
            scan_generated_cosmosdb_load_files()

        else:
            print_options('Error: invalid function: {}'.format(func))
    else:
            print_options('Error: no command-line arguments')
