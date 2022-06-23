"""
Usage:
  python main.py <func>
  python main.py create_module Thing
Options:
  -h --help     Show this screen.
  --version     Show version.
"""

__author__  = 'Chris Joakim'
__email__   = "chjoakim@microsoft.com"
__license__ = "MIT"
__version__ = "2022/06/23"

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


def print_options(msg):
    print(msg)
    arguments = docopt(__doc__, version=__version__)
    print(arguments)

def transform_original_bom_data():
    print('transform_original_bom_data')
    print("==========\ncheck_bytes:")
    docker_dmg_size = 707758073
    kb = Bytes.kilobyte()
    print('kb: {}'.format(kb))
    print('docker_dmg as KB: {}'.format(Bytes.as_kilobytes(docker_dmg_size)))
    print('docker_dmg as MB: {}'.format(Bytes.as_megabytes(docker_dmg_size)))
    print('docker_dmg as GB: {}'.format(Bytes.as_gigabytes(docker_dmg_size)))
    print('docker_dmg as TB: {}'.format(Bytes.as_terabytes(docker_dmg_size)))
    print('docker_dmg as PB: {}'.format(Bytes.as_petabytes(docker_dmg_size)))

def check_env():
    print("==========\ncheck_env:")
    home = Env.var('HOME')
    print('home: {}'.format(home))

def check_excel():
    print("==========\ncheck_excel:")
    x = Excel()
    title = 'My Repos'
    repos = FS.read_json('data/nc_zipcodes.json')
    attrs = 'postal_cd,country_cd,city_name,state_abbrv,latitude,longitude'.split(',')
    outfile = 'tmp/nc_zipcodes.xlsx'
    x.generate(title, repos, attrs, outfile)

def check_fs():
    print("==========\ncheck_fs:")
    pwd = FS.pwd()
    print('pwd: {}'.format(pwd))
    files = FS.walk(pwd)
    for file in files:
        if 'cj-py/pysrc' in file['dir']:
            if file['base'].endswith('.py'):
                print(file['full'])
    print('count: {}'.format(len(files)))

    infile = 'data/postal_codes_nc.csv'
    rows = FS.read_csvfile_into_rows(infile, delim=',')
    for idx, row in enumerate(rows):
        if idx < 5:
            print(row)

    objects = FS.read_csvfile_into_objects(infile, delim=',')
    for idx, obj in enumerate(objects):
        if idx < 5:
            print(obj)

def check_adl():
    print("==========\ncheck_adl:")
    fsname, dirname, adl = 'testfs', 'testdir', Adl()

    fs_list = adl.filesystem_list()
    for fs in fs_list:
        print('fs: {}'.format(fs.name))

    adl.delete_fs(fsname)
    adl.delete_fs(fsname)
    time.sleep(5)
    adl.create_fs(fsname)
    adl.create_fs(fsname)
    time.sleep(5)
    adl.create_dir(fsname, dirname)
    adl.create_dir(fsname, dirname)
    time.sleep(5)
    dir_client = adl.directory_client(fsname, dirname)
    print(dir_client)
    adl.upload_file(dir_client, 'requirements.in', 'requirements')
    adl.upload_file(dir_client, 'pysrc/cjcc/env.py', 'env.py')
    time.sleep(5)
    adl.download_file(dir_client, 'requirements', 'tmp/requirements_downloaded')
    time.sleep(5)
    file_list = adl.file_list(fsname, dirname)
    for item in file_list:
        print('item: {} {}'.format(item.name, item))

def check_storage():
    print("==========\ncheck_storage:")
    cname, stor = 'smoketest', Storage()
    stor.delete_container(cname)
    stor.delete_container(cname)
    stor.create_container(cname)
    stor.create_container(cname)
    time.sleep(8)
    stor.upload_blob('pysrc/env.py', cname, 'env.py')
    time.sleep(8)
    blob_list = stor.list_container(cname)
    for item in blob_list:
        print('blob: {} {}'.format(item.name, item))
    stor.download_blob(cname, 'env.py', 'tmp/env_downloaded.py', )
    clist = stor.list_containers()
    for item in clist:
        print('container: {} {}'.format(item.name, item))

def check_rcache():
    print("==========\ncheck_rcache:")
    rcache = RCache('localhost', 6379)
    e1 = str(Env.epoch())
    rcache.set('epoch', e1)
    e2 = rcache.get('epoch').decode("utf-8")
    print('redis epoch 1: {}'.format(e1))
    print('redis epoch 2: {}'.format(e2))

def check_mongo():
    print("==========\ncheck_mongo:")
    opts = dict()
    opts['host'] = 'localhost'
    opts['port'] = 27017
    m = Mongo(opts)
    db = m.set_db('dev')
    coll = m.set_coll('movies')
    movies = FS.read_json('data/movies.json')
    keys = sorted(movies.keys())
    for idx, key in enumerate(keys):
        if idx < 100:
            data = dict()
            data['title_id'] = key
            data['title'] = movies[key]
            data['doctype'] = 'movie'
            if idx < 12:
                data['top10'] = True
            else:
                data['top10'] = False
            result = m.insert_doc(data)
            #print('{} -> {}'.format(str(result.inserted_id), str(data)))
            print(data)
    print(m.list_collections())
    print(m.list_databases())
    print(m.find_one({"title": 'Footloose'}))
    print(m.find_one({"title": 'Not There'}))
    print(m.find_by_id('5ea575f08bd3a96405ea6366'))

    um = m.update_many({"top10": True}, {'$set': {"rating": 100, "bacon": False}}, False)
    print(um)
    fl2 = m.update_one({"title": 'Footloose'}, {'$set': {"rating": 100, "bacon": True}}, False) # update_one(filter, update, upsert)
    print(fl2)
    fl3 = m.find_one({"title": 'Footloose'})
    print(fl3)
    cursor = m.find({"top10": True})
    for doc in cursor:
        print(doc)

    print(m.count_docs({}))
    print(m.count_docs({"title": 'Footloose'}))
    print(m.delete_by_id('5ea575f08bd3a96405ea6366'))
    print(m.count_docs({}))
    print(m.delete_one({"title": 'The Money Pit'}))
    print(m.count_docs({}))
    print(m.delete_many({"doctype": 'movie'}))
    print(m.count_docs({}))

def check_cosmos():
    print("==========\ncheck_cosmos:")
    opts = dict()
    opts['url'] = Env.var('AZURE_COSMOSDB_SQLDB_URI')
    opts['key'] = Env.var('AZURE_COSMOSDB_SQLDB_KEY')
    dbname, cname = 'dev', 'smoke_test'

    c = Cosmos(opts)

    print('disable/enable metrics, print_record_diagnostics:')
    c.disable_query_metrics()
    c.enable_query_metrics()
    c.reset_record_diagnostics()
    c.print_record_diagnostics()
    c.print_last_request_charge()

    print('list_databases:')
    for db in c.list_databases():
        print('database: {}'.format(db['id']))   
    c.print_last_request_charge()

    print('set_db:')
    dbproxy = c.set_db(dbname)
    c.print_last_request_charge()

    print('list_containers:')
    for con in c.list_containers():
        print('container: {}'.format(con['id']))    
    c.print_last_request_charge()

    print('delete_container:')
    c.delete_container(cname)
    c.print_last_request_charge()

    print('create_container:')
    ctrproxy = c.create_container(cname, '/pk', 500)
    c.print_last_request_charge()

    print('create_container:')
    ctrproxy = c.create_container(cname, '/pk', 500)
    c.print_last_request_charge()

    print('set_container:')
    ctrproxy = c.set_container(cname)
    c.print_last_request_charge()
    
    print('update_container_throughput:')
    offer = c.update_container_throughput(cname, 600)
    c.print_last_request_charge()

    print('get_container_offer:')
    offer = c.get_container_offer(cname)
    c.print_last_request_charge()

    infile = 'data/postal_codes_nc.csv'
    objects = FS.read_csvfile_into_objects(infile, delim=',')
    documents = list()
    ctrproxy = c.set_container(cname)

    print('upsert_docs:')
    for idx, obj in enumerate(objects):
        del obj['id']
        if idx < 10:
            obj['pk'] = obj['postal_cd']
            print(obj)
            result = c.upsert_doc(obj)
            documents.append(result)
            c.print_last_request_charge()

    for idx, doc in enumerate(documents):
        if idx < 3:
            result = c.delete_doc(doc, doc['pk'])
            print('delete result: {}'.format(result))
            c.print_last_request_charge()
        else:
            doc['updated'] = True
            result = c.upsert_doc(doc)
            print('update result: {}'.format(result))
            c.print_last_request_charge()

    sql = "select * from c where c.state_abbrv = 'NC'"
    print('query; sql: {}'.format(sql))
    items = c.query_container(cname, sql, True, 1000)
    c.print_last_request_charge()
    last_id, last_pk = None, None
    for item in items:
        last_id = item['id']
        last_pk = item['pk']
        print(json.dumps(item, sort_keys=False, indent=2))

    print('read_doc; id: {} pk: {}'.format(last_id, last_pk))
    doc = c.read_doc(cname, last_id, last_pk)
    print(doc)
    c.print_record_diagnostics()
    c.print_last_request_charge()

    print('record_diagnostics_headers_dict:')
    print(json.dumps(c.record_diagnostics_headers_dict(), sort_keys=True, indent=2))
    
    print('reset and print diagnostics')
    c.reset_record_diagnostics()
    c.print_record_diagnostics()

    print('delete container: not_there')
    c.delete_container('not_there')
    c.print_last_request_charge()

    print('delete container: {}'.format(cname))
    c.delete_container(cname)
    c.print_last_request_charge()

def create_module(classname):
    root_dir = FS.pwd()
    values = dict()
    values['classname'] = classname
    values['modulename'] = classname.lower()

    t = Template.get_template(root_dir, 'python_module.txt')
    code = Template.render(t, values)
    codefile = 'pysrc/{}.py'.format(classname.lower())
    FS.write(codefile, code, verbose=True)

    t = Template.get_template(root_dir, 'python_test.txt')
    code = Template.render(t, values)
    codefile = 'tests/test_{}.py'.format(classname.lower())
    FS.write(codefile, code, verbose=True)

def check_eventhub_send():
    opts = dict()
    opts['conn_str'] = Env.var('AZURE_EVENTHUB_CONN_STRING')
    opts['hub_name'] = Env.var('AZURE_EVENTHUB_HUBNAME')
    opts['type']     = 'producer'
    opts['verbose']  = True
    print(opts)
    zipcodes = FS.read_json('data/nc_zipcodes.json')
    eh = None
    
    try:
        eh = EventHub(opts)
        for idx, z in enumerate(zipcodes):
            if idx < 10:
                z['sent_index'] = idx
                z['sent_epoch'] = Env.epoch()
                batch = list()
                batch.append(z)
                print('=== main; batch: {}'.format(json.dumps(batch, sort_keys=False, indent=2)))
                eh.send_messages(batch)
                #time.sleep(1)
    finally:
        if eh:
            eh.close()

def timezone_chart():
    # https://www.timeanddate.com/time/map/
    # https://www.timeanddate.com/time/zone/india

    print('timezone_chart')
    csv_lines = list()

    tzones = Tz.common_timezone_list()
    for x in tzones:
        pass # print(x)

    hours = range(0, 24)

    timezones = dict()
    timezones['Australia/Sydney'] = 11
    timezones['Asia/Tokyo']       = 9
    timezones['Australia/Perth']  = 8
    timezones['India']            = 5.5
    timezones['Europe/Paris']     = 1
    timezones['GMT']              = 0 
    timezones['Europe/Paris']     = 1
    timezones['US/Eastern']       = -5 
    timezones['US/Central']       = -6 
    timezones['US/Mountain']      = -7 
    timezones['US/Pacific']       = -8 
    timezones['US/Hawaii']        = -10 

    tz_keys = timezones.keys()
    csv_lines.append(",".join(tz_keys))

    for h in hours:
        csv_row = list()
        for tz_name in tz_keys:
            offset = timezones[tz_name]
            hour = h + offset
            if hour < 0:
                hour = hour + 24
            elif hour > 23:
                hour = hour - 24
            csv_row.append(str(hour))
        csv_lines.append(",".join(csv_row))

    content = "\n".join(csv_lines)
    FS.write('tmp/timezones.csv', content, verbose=True)


if __name__ == "__main__":

    # dispatch to a main function based either on the first command-line arg,
    # or on the MAIN_PY_FUNCTION environment variable when run as a container.

    func = sys.argv[1].lower()

    if func == 'adl':
        check_adl()
    elif func == 'bytes':
        check_bytes()
    elif func == 'cosmos':
        check_cosmos()
    elif func == 'env':
        check_env()
    elif func == 'eventhub_send':
        check_eventhub_send()
    elif func == 'excel':
        check_excel()
    elif func == 'fs':
        check_fs()
    elif func == 'mongo':
        check_mongo()
    elif func == 'rcache':
        check_rcache()
    elif func == 'storage':
        check_storage()
    elif func == 'create_module':
        classname = sys.argv[2]
        create_module(classname)
    elif func == 'timezone_chart':
        timezone_chart()
    else:
        print_options('Error: invalid function: {}'.format(func))

