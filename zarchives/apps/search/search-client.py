"""
Usage:
    python search-client.py display_env
    -
    python search-client.py create_blob_datasource documents
    python search-client.py create_cosmos_datasource dev airports
    python search-client.py delete_datasource azureblob-documents
    -
    python search-client.py list_indexes
    python search-client.py list_indexers
    python search-client.py list_datasources
    python search-client.py list_skillsets
    -
    python search-client.py get_index airports
    python search-client.py get_indexer airports
    python search-client.py get_indexer_status airports
    python search-client.py get_datasource azureblob-documents
    python search-client.py get_skillset xxx
    -
    python search-client.py create_index documents documents_index_v1
    python search-client.py delete_index documents
    python search-client.py create_index airports airports_index
    -
    python search-client.py create_indexer documents documents_indexer_v1
    python search-client.py reset_indexer documents
    python search-client.py run_indexer airports
    python search-client.py delete_indexer documents
    python search-client.py create_indexer airports airports_indexer
    -
    python search-client.py create_synmap synmap synonym_map_v1
    python search-client.py update_synmap synmap synonym_map_v1
    python search-client.py delete_synmap synmap 
    -
    python search-client.py create_skillset skillset skillset_v1
    python search-client.py delete_skillset skillset 
    -
    python search-client.py search_index airports all_airports
    python search-client.py search_index airports airports_charl
    python search-client.py search_index airports airports_clt
    python search-client.py search_index airports airports_lucene_east_cl_south 
    python search-client.py search_index documents top_words_flanagan
    python search-client.py search_index documents us_dot_number
    python search-client.py search_index documents pandas_as_in_bear
    python search-client.py search_index documents pandas_as_in_python
    -
    python search-client.py lookup_doc documents aHR0cHM6Ly9jam9ha2ltc2VhcmNoLmJsb2IuY29yZS53aW5kb3dzLm5ldC9kb2N1bWVudHMvc2ZueS5qcGc1
    -
    python search-client.py index_schema_diff schemas/documents_index_v1.json schemas/documents_index_v2.json
    python search-client.py indexer_schema_diff schemas/documents_indexer_v1.json schemas/documents_indexer_v2.json
    -
    python search-client.py invoke_local_function
    python search-client.py invoke_azure_function
    -
    python search-client.py generate_sample_index_schema_file
    python search-client.py generate_sample_blob_indexer
    python search-client.py generate_airport_schema_files
    -
"""

__author__  = 'Chris Joakim'
__email__   = "chjoakim@microsoft.com"
__license__ = "MIT"
__version__ = "December 2021"

# https://docs.microsoft.com/en-us/rest/api/searchservice/
# https://docs.microsoft.com/en-us/rest/api/searchservice/search-documents
# https://docs.microsoft.com/en-us/azure/search/search-get-started-python
# https://docs.microsoft.com/en-us/azure/search/search-howto-index-cosmosdb
# https://requests.readthedocs.io/en/master/user/quickstart/

import json
import os
import sys
import time
import requests

from docopt import docopt

from base import BaseClass
from schemas import Schemas
from urls import Urls


class SearchClient(BaseClass):

    def __init__(self):
        BaseClass.__init__(self)
        self.u = None  # the current url
        self.r = None  # the current requests response object
        self.config = dict()
        self.schemas = Schemas()
        self.urls = Urls()
        self.user_agent = {'User-agent': 'Mozilla/5.0'}
        self.search_name = os.environ['AZURE_SEARCH_NAME']
        self.search_url  = os.environ['AZURE_SEARCH_URL']
        self.search_admin_key = os.environ['AZURE_SEARCH_ADMIN_KEY']
        self.search_query_key = os.environ['AZURE_SEARCH_QUERY_KEY']
        self.search_api_version = 'api-version=2020-06-30'
        self.named_searches = self.named_searches_dict()

        self.admin_headers = dict()
        self.admin_headers['Content-Type'] = 'application/json'
        self.admin_headers['api-key'] = self.search_admin_key

        self.query_headers = dict()
        self.query_headers['Content-Type'] = 'application/json'
        self.query_headers['api-key'] = self.search_query_key

    def display_env(self):
        print('search_name:      {}'.format(self.search_name))
        print('search_url:       {}'.format(self.search_url))
        print('search_admin_key: {}'.format(self.search_admin_key))
        print('search_query_key: {}'.format(self.search_query_key))
        print('admin_headers:\n{}'.format(json.dumps(self.admin_headers, sort_keys=False, indent=2)))
        print('query_headers:\n{}'.format(json.dumps(self.query_headers, sort_keys=False, indent=2)))

    def list_indexes(self):
        url = self.urls.list_indexes()
        self.invoke('list_indexes', 'get', url, self.admin_headers)

    def list_indexers(self):
        url = self.urls.list_indexers()
        self.invoke('list_indexers', 'get', url, self.admin_headers)

    def list_datasources(self):
        url = self.urls.list_datasources()
        self.invoke('list_datasources', 'get', url, self.admin_headers)

    def list_skillsets(self):
        url = self.urls.list_skillsets()
        self.invoke('list_skillsets', 'get', url, self.admin_headers)

    def get_index(self, name):
        url = self.urls.get_index(name)
        self.invoke('get_index', 'get', url, self.admin_headers)

    def get_indexer(self, name):
        url = self.urls.get_indexer(name)
        self.invoke('get_indexer', 'get', url, self.admin_headers)

    def get_indexer_status(self, name):
        url = self.urls.get_indexer_status(name)
        self.invoke('get_indexer_status', 'get', url, self.admin_headers)

    def get_datasource(self, name):
        url = self.urls.get_datasource(name)
        self.invoke('get_datasource', 'get', url, self.admin_headers)

    def get_skillset(self, name):
        url = self.urls.get_skillset(name)
        self.invoke('get_skillset', 'get', url, self.admin_headers)

    def create_index(self, name, schema_file):
        self.modify_index('create', name, schema_file)

    def update_index(self, name, schema_file):
        self.modify_index('update', name, schema_file)

    def delete_index(self, name):
        self.modify_index('delete', name, None)

    def modify_index(self, action, name, schema_file):
        # read the schema json file if necessary
        schema = None
        if action in ['create', 'update']:
            schema = self.schemas.read(schema_file, {'name': name})

        if action == 'create':
            http_method = 'post'
            url = self.urls.create_index()
        elif action == 'update':
            http_method = 'put'
            url = self.urls.modify_index(name)
        elif action == 'delete':
            http_method = 'delete'
            url = self.urls.modify_index(name)

        function = '{}_index_{}'.format(action, name)
        self.invoke(function, http_method, url, self.admin_headers, schema)

    def create_indexer(self, name, schema_file):
        self.modify_indexer('create', name, schema_file)

    def update_indexer(self, name, schema_file):
        self.modify_indexer('update', name, schema_file)

    def delete_indexer(self, name):
        self.modify_indexer('delete', name, None)

    def modify_indexer(self, action, name, schema_file):
        # read the schema json file if necessary
        schema = None
        if action in ['create', 'update']:
            schema = self.schemas.read(schema_file, {'name': name})

        if action == 'create':
            http_method = 'post'
            url = self.urls.create_indexer()
        elif action == 'update':
            http_method = 'put'
            url = self.urls.modify_indexer(name)
        elif action == 'delete':
            http_method = 'delete'
            url = self.urls.modify_indexer(name)

        function = '{}_indexer_{}'.format(action, name)
        self.invoke(function, http_method, url, self.admin_headers, schema)

    def reset_indexer(self, name):
        url = self.urls.reset_indexer(name)
        self.invoke('reset_indexer', 'post', url, self.admin_headers)

    def run_indexer(self, name):
        url = self.urls.run_indexer(name)
        self.invoke('run_indexer', 'post', url, self.admin_headers)

    def create_blob_datasource(self, container):
        body = self.schemas.blob_datasource_post_body()
        body['name'] = self.blob_datasource_name(container)
        body['credentials']['connectionString'] = self.stor_acct_conn_str
        body['container']['name'] = container
        print(json.dumps(body, sort_keys=False, indent=2))
        if True:
            url = self.urls.create_datasource()
            function = 'create_blob_datasource_{}'.format(container)
            self.invoke(function, 'post', url, self.admin_headers, body)

    def create_cosmos_datasource(self, dbname, container):
        conn_str = self.cosmos_datasource_name_conn_str(dbname)
        body = self.schemas.cosmosdb_datasource_post_body()
        body['name'] = self.cosmos_datasource_name(dbname, container)
        body['credentials']['connectionString'] = conn_str
        body['container']['name'] = container
        print(json.dumps(body, sort_keys=False, indent=2))
        if True:
            url = self.urls.create_datasource()
            function = 'create_cosmos_datasource_{}_{}'.format(dbname, container)
            self.invoke(function, 'post', url, self.admin_headers, body)

    def delete_datasource(self, name):
        url = self.urls.modify_datasource(name)
        function = 'delete_datasource{}'.format(name)
        self.invoke(function, 'delete', url, self.admin_headers, None)

    def create_synmap(self, name, schema_file):
        self.modify_synmap('create', name, schema_file)

    def update_synmap(self, name, schema_file):
        self.modify_synmap('update', name, schema_file)

    def delete_synmap(self, name):
        self.modify_synmap('delete', name, None)

    def modify_synmap(self, action, name, schema_file):
        # read the schema json file if necessary
        schema = None
        if action in ['create', 'update']:
            schema_file = 'schemas/{}.json'.format(schema_file)
            schema = self.load_json_file(schema_file)
            schema['name'] = name

        if action == 'create':
            http_method = 'post'
            url = self.urls.create_synmap()
        elif action == 'update':
            http_method = 'put'
            url = self.urls.modify_synmap(name)
        elif action == 'delete':
            http_method = 'delete'
            url = self.urls.modify_synmap(name)

        function = '{}_synmap_{}'.format(action, name)
        self.invoke(function, http_method, url, self.admin_headers, schema)

    def create_skillset(self, name, schema_file):
        self.modify_skillset('create', name, schema_file)

    def update_skillset(self, name, schema_file):
        self.modify_skillset('update', name, schema_file)

    def delete_skillset(self, name):
        self.modify_skillset('delete', name, None)

    def modify_skillset(self, action, name, schema_file):
        # read the schema json file if necessary
        schema = None
        if action in ['create', 'update']:
            schema_file = 'schemas/{}.json'.format(schema_file)
            schema = self.load_json_file(schema_file)
            schema['name'] = name
            schema['cognitiveServices']['key'] = os.environ['AZURE_SEARCH_COGSVCS_ALLIN1_KEY']

            for skill in schema['skills']:
                t = skill['@odata.type']
                if t == "#Microsoft.Skills.Custom.WebApiSkill":
                    skill['uri'] = self.azure_function_url('azure')

        if action == 'create':
            http_method = 'post'
            url = self.urls.create_skillset()
        elif action == 'update':
            http_method = 'put'
            url = self.urls.modify_skillset(name)
        elif action == 'delete':
            http_method = 'delete'
            url = self.urls.modify_skillset(name)

        function = '{}_skillset_{}'.format(action, name)
        self.invoke(function, http_method, url, self.admin_headers, schema)

    def search_index(self, idx_name, search_name, additional):
        print('---')
        print('search_index: {} -> {} | {}'.format(idx_name, search_name, additional))
        url = self.urls.search_index(idx_name)
        print('search_index url: {}'.format(url))
        #print('defined searches: {}'.format(self.named_searches.keys()))

        if search_name in self.named_searches.keys(): 
            search_params = self.named_searches[search_name]
            print('named_search found: {}  params: {}'.format(search_name, search_params))
        else:
            if idx_name == 'airports':
                search_params = self.named_searches['all_airports']
            else:
                search_params = self.named_searches['all_documents']
            print('named_search not found: {}  using default params: {}'.format(search_name, search_params)) 

        print('url:     {}'.format(url))
        print('method:  {}'.format('POST'))
        print('params:  {}'.format(search_params))
        print('headers: {}'.format(self.admin_headers))

        r = requests.post(url=url, headers=self.admin_headers, json=search_params)
        print('response: {}'.format(r))
        if r.status_code == 200:
            resp_obj = json.loads(r.text)
            print(json.dumps(resp_obj, sort_keys=False, indent=2))
            print('response document count: {}'.format(resp_obj['@odata.count']))
            outfile = 'tmp/{}.json'.format(search_name)
            self.write_json_file(resp_obj, outfile)

    def named_searches_dict(self):
        if False:
            searches = dict()
            searches['all_airports'] = {'count': True, 'search': '*', 'orderby': 'pk'}
            searches['all_airports_charl'] = {'count': True, 'search': 'charl*', 'orderby': 'pk', 'select': 'name,city,pk'}
            searches['all_airports_charl_lucene'] = {'count': True, 'search': 'charl*', 'orderby': 'pk', 'select': 'name,city,pk', 'queryType': 'full'}
            searches['all_documents'] = {'count': True, 'search': '*', 'orderby': 'id'}
            searches['top_words_'] = {'count': True, 'search': '*', 'orderby': 'id'}
            self.write_json_file(searches, 'searches_generated.json')
        else:
            searches = self.load_json_file('searches.json')
        return searches

    def lookup_doc(self, index_name, doc_key):
        print('lookup_doc: {} {}'.format(index_name, doc_key))
        # See https://docs.microsoft.com/en-us/rest/api/searchservice/lookup-document#examples
        # GET /indexes/hotels/docs/2?api-version=2020-06-30
        url = self.urls.lookup_doc(index_name, doc_key)
        headers = self.query_headers
        print(url)
        print(headers)
        function = 'lookup_doc_{}_{}'.format(index_name, doc_key)
        r = self.invoke(function, 'get', url, self.query_headers)

    def invoke(self, function_name, method, url, headers={}, json_body={}):
        # This is a generic method which invokes all HTTP Requests to the Azure Search Service
        print('===')
        print("invoke: {} {} {}\nheaders: {}\nbody: {}".format(
            function_name, method.upper(), url, headers, json_body))
        print('---')
        if method == 'get':
            r = requests.get(url=url, headers=headers)
        elif method == 'post':
            r = requests.post(url=url, headers=headers, json=json_body)
        elif method == 'put':
            r = requests.put(url=url, headers=headers, json=json_body)
        elif method == 'delete':
            r = requests.delete(url=url, headers=headers)
        else:
            print('error; unexpected method value passed to invoke: {}'.format(method))

        print('response: {}'.format(r))
        if r.status_code < 300:
            try:
                resp_obj = json.loads(r.text)
                outfile = 'tmp/{}.json'.format(function_name)
                self.write_json_file(resp_obj, outfile)
            except Exception as e:
                print("exception processing http response".format(e))
                print(r.text)
        else:
            print(r.text)
        return r

    def epoch(self):
        return time.time()
    
    def write_json_file(self, obj, outfile):
        with open(outfile, 'wt') as f:
            f.write(json.dumps(obj, sort_keys=False, indent=2))
            print('file written: {}'.format(outfile))

    def load_json_file(self, infile):
        with open(infile, 'rt') as json_file:
            return json.loads(str(json_file.read()))

    def generate_sample_index_schema_file(self):
        schema = self.schemas.sample_index_object('sample')
        self.write_json_file(schema, 'schemas/sample_index.json')

    def generate_airport_schema_files(self):
        index_name = 'airports'
        indexer_name = 'airports'
        dbname, container = 'dev', 'airports'
        datasource_name = self.cosmos_datasource_name(dbname, container)

        schema = self.schemas.airports_index_schema(index_name)
        self.write_json_file(schema, 'schemas/airports_index.json')

        schema = self.schema.indexer_schema(indexer_name, index_name, datasource_name)
        self.write_json_file(schema, 'schemas/airports_indexer.json')

    def generate_sample_blob_indexer(self):
        schema = self.schemas.sample_blob_indexer()
        self.write_json_file(schema, 'schemas/sample_blob_indexer.json')

    def index_schema_diff(self, file1, file2):
        diffs = self.schemas.index_schema_diff(file1, file2)
        print(json.dumps(diffs, sort_keys=False, indent=2))

    def indexer_schema_diff(self, file1, file2):
        diffs = self.schemas.indexer_schema_diff(file1, file2)
        print(json.dumps(diffs, sort_keys=False, indent=2))

    def azure_function_url(self, target):
        if str(target).lower() == 'local':
            # return a value like 'http://localhost:7071/api/TopWordsSkill'
            return os.environ['AZURE_FUNCTION_CUSTOM_SKILL_LOCAL']
        else:
            # return a value like 'https://cjoakimsearchapp.azurewebsites.net/api/TopWordsSkill?code=nXc ... z7FEA=='
            return os.environ['AZURE_FUNCTION_CUSTOM_SKILL_REMOTE']

    def invoke_local_function(self):
        url = self.azure_function_url('local')
        self.invoke_function(url, 'local')
    
    def invoke_azure_function(self):
        url = self.azure_function_url('azure')
        self.invoke_function(url, 'azure')

    def invoke_function(self, url, target):
        function = 'invoke_{}_function'.format(target)
        post_data = self.load_json_file('data/sample_skill_function_post_body.json')
        print('request:')
        print(json.dumps(post_data, sort_keys=False, indent=2))
        r = self.invoke(function, 'post', url, self.admin_headers, post_data)
        print('response:')
        resp_obj = json.loads(r.text)
        print(json.dumps(resp_obj, sort_keys=False, indent=2))

    def read_sample_merged_data(self, sample_name):
        samples_file = 'data/test_merged_text.json'
        merged_text = 'this is some default text, repeat default, only a default.'
        samples = self.load_json_file(samples_file)
        for sample in samples:
            if sample['file_name'] == sample_name:
                return sample['mergedText']
        return merged_text


def print_options(msg):
    print(msg)
    arguments = docopt(__doc__, version=__version__)
    print(arguments)


if __name__ == "__main__":

    if len(sys.argv) > 1:
        func = sys.argv[1].lower()
        print('func: {}'.format(func))
        client = SearchClient()

        if func == 'display_env':
            client.display_env()

        elif func == 'generate_sample_index_schema_file':
            client.generate_sample_index_schema_file()

        elif func == 'generate_sample_blob_indexer':
            client.generate_sample_blob_indexer()

        elif func == 'generate_airport_schema_files':
            client.generate_airport_schema_files()

        elif func == 'list_indexes':
            client.list_indexes()

        elif func == 'list_indexers':
            client.list_indexers()

        elif func == 'list_datasources':
            client.list_datasources()

        elif func == 'list_skillsets':
            client.list_skillsets()

        elif func == 'get_index':
            name = sys.argv[2]
            client.get_index(name)

        elif func == 'get_indexer':
            name = sys.argv[2]
            client.get_indexer(name)

        elif func == 'get_indexer_status':
            name = sys.argv[2]
            client.get_indexer_status(name)

        elif func == 'get_datasource':
            name = sys.argv[2]
            client.get_datasource(name)

        elif func == 'get_skillset':
            name = sys.argv[2]
            client.get_skillset(name)

        elif func == 'create_index':
            index_name = sys.argv[2]
            schema_file = sys.argv[3]
            client.create_index(index_name, schema_file)

        elif func == 'update_index':
            index_name = sys.argv[2]
            schema_file = sys.argv[3]
            client.update_index(index_name, schema_file)

        elif func == 'delete_index':
            name = sys.argv[2]
            client.delete_index(name)

        elif func == 'create_indexer':
            indexer_name = sys.argv[2]
            schema_file = sys.argv[3]
            client.create_indexer(indexer_name, schema_file)

        elif func == 'update_indexer':
            indexer_name = sys.argv[2]
            schema_file = sys.argv[3]
            client.update_indexer(indexer_name, schema_file)

        elif func == 'delete_indexer':
            name = sys.argv[2]
            client.delete_indexer(name)

        elif func == 'reset_indexer':
            name = sys.argv[2]
            client.reset_indexer(name)

        elif func == 'run_indexer':
            name = sys.argv[2]
            client.run_indexer(name)

        elif func == 'create_blob_datasource':
            container = sys.argv[2]
            client.create_blob_datasource(container)

        elif func == 'create_cosmos_datasource':
            dbname = sys.argv[2]
            container = sys.argv[3]
            client.create_cosmos_datasource(dbname, container)

        elif func == 'delete_datasource':
            name = sys.argv[2]
            client.delete_datasource(name)

        elif func == 'create_blob_indexer':
            datasource_name = sys.argv[2]
            target_index_name = sys.argv[3]
            client.create_blob_indexer(datasource_name, target_index_name)

        elif func == 'create_synmap':
            synmap_name = sys.argv[2]
            schema_file = sys.argv[3]
            client.create_synmap(synmap_name, schema_file)

        elif func == 'update_synmap':
            synmap_name = sys.argv[2]
            schema_file = sys.argv[3]
            client.update_synmap(synmap_name, schema_file)

        elif func == 'delete_synmap':
            synmap_name = sys.argv[2]
            client.delete_synmap(synmap_name)

        elif func == 'create_skillset':
            skillset_name = sys.argv[2]
            schema_file = sys.argv[3]
            client.create_skillset(skillset_name, schema_file)

        elif func == 'update_skillset':
            skillset_name = sys.argv[2]
            schema_file = sys.argv[3]
            client.update_skillset(skillset_name, schema_file)

        elif func == 'delete_skillset':
            skillset_name = sys.argv[2]
            client.delete_skillset(skillset_name)

        elif func == 'index_schema_diff':
            file1 = sys.argv[2]
            file2 = sys.argv[3]
            client.index_schema_diff(file1, file2)

        elif func == 'indexer_schema_diff':
            file1 = sys.argv[2]
            file2 = sys.argv[3]
            client.indexer_schema_diff(file1, file2)

        elif func == 'invoke_local_function':
            client.invoke_local_function()

        elif func == 'invoke_azure_function':
            client.invoke_azure_function()

        elif func == 'search_index':
            index_name  = sys.argv[2]
            search_name = sys.argv[3]
            additional  = None
            if len(sys.argv) > 4:
                additional = sys.argv[4]
            client.search_index(index_name, search_name, additional)

        elif func == 'lookup_doc':
            index_name  = sys.argv[2]
            doc_key     = sys.argv[3]
            client.lookup_doc(index_name, doc_key)

        else:
            print_options('Error: invalid function: {}'.format(func))
    else:
        print_options('Error: no function argument provided.')
