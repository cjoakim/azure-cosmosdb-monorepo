__author__  = 'Chris Joakim'
__email__   = "chjoakim@microsoft.com"
__license__ = "MIT"
__version__ = "November 2021"

import json

from schemas import Schemas


def test_blob_datasource_post_body():
    s = Schemas()
    body = s.blob_datasource_post_body()
    jstr = json.dumps(body, sort_keys=True)
    expected = '{"container": {"name": "... populate me ..."}, "credentials": {"connectionString": "... populate me ..."}, "name": "... populate me ...", "type": "azureblob"}'
    #print(jstr)
    assert(expected == jstr)

def test_cosmosdb_datasource_post_body():
    s = Schemas()
    body = s.cosmosdb_datasource_post_body()
    jstr = json.dumps(body, sort_keys=True)
    expected = '{"container": {"name": "... populate me ...", "query": null}, "credentials": {"connectionString": "... populate me ..."}, "dataChangeDetectionPolicy": {"@odata.type": "#Microsoft.Azure.Search.HighWaterMarkChangeDetectionPolicy", "highWaterMarkColumnName": "_ts"}, "name": "... populate me ...", "type": "cosmosdb"}'
    #print(jstr)
    assert(expected == jstr)

def test_read():
    s = Schemas()
    schema = s.read('documents_index_v1', {'name': 'test'})
    #print(schema)
    assert (len(schema['fields']) == 17)
    assert (schema['name'] == 'test')
    assert (schema['fields'][0]['name'] == 'id')
    assert (schema['fields'][0]['type'] == 'Edm.String')
    assert (schema['fields'][-1]['name'] == 'topwords')
    assert (schema['fields'][-1]['type'] == 'Collection(Edm.String)')

def test_indexer_schema():
    s = Schemas()
    indexer_name = 'indexer'
    index_name = 'index'
    datasource_name = 'datasource'
    schema = s.indexer_schema(indexer_name, index_name, datasource_name)
    #print(schema)
    assert (schema['name'] == indexer_name)
    assert (schema['dataSourceName'] == datasource_name)
    assert (schema['targetIndexName'] == index_name)
    assert (schema['schedule'] == { "interval" : "PT2H" })
