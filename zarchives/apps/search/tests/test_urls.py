__author__  = 'Chris Joakim'
__email__   = "chjoakim@microsoft.com"
__license__ = "MIT"
__version__ = "November 2021"

import os

from urllib.parse import urlparse

from urls import Urls

BASE_URL = os.environ['AZURE_SEARCH_URL']  # example: https://cjoakimsearch.search.windows.net
EXPECTED_VERSION_LITERAL = 'api-version=2020-06-30'

def path(full_url):
    idx = len(BASE_URL)
    return full_url[idx:999]

def valid_url(s):
    # >>> from urllib.parse import urlparse
    # >>> result = urlparse('https://cjoakimsearch.search.windows.net/indexes?api-version=2020-06-30')
    # >>> result
    # ParseResult(scheme='https', netloc='cjoakimsearch.search.windows.net', path='/some/nested/path/for/testing',
    #             params='', query='x=7', fragment='')
    # >>> result = urlparse('https://cjoakimsearch.search.windows.net/indexes?api-version=2020-06-30')
    # >>> result
    # ParseResult(scheme='https', netloc='cjoakimsearch.search.windows.net', path='/indexes', params='',
    #             query='api-version=2020-06-30', fragment='')

    try:
        result = urlparse(s)
        if result.scheme != 'https':
            return False
        if len(result.netloc) < 20:
            return False
        if not result.netloc.endswith('.search.windows.net'):
            return False
        return True
    except:
        return False

def valid_version(s):
    result = urlparse(s)
    try:
        if EXPECTED_VERSION_LITERAL in result.query:
            return True
        else:
            return False
    except:
        return False

def test_base_url_env_var():
    assert(BASE_URL.startswith('https://'))

def test_path_helper():
    full_url = 'https://cjoakimsearch.search.windows.net/some/nested/path/for/testing?x=7'
    p = path('https://cjoakimsearch.search.windows.net/some/nested/path/for/testing?x=7')
    assert(p == '/some/nested/path/for/testing?x=7')

def test_list_indexes():
    url = Urls().list_indexes()
    print('url: ' + url)
    assert(valid_url(url))
    assert(valid_version(url))
    assert(path(url) == '/indexes?api-version=2020-06-30')

def test_list_indexers():
    url = Urls().list_indexers()
    print('url: ' + url)
    assert(valid_url(url))
    assert(valid_version(url))
    assert(path(url) == '/indexers?api-version=2020-06-30')

def test_list_datasources():
    url = Urls().list_datasources()
    print('url: ' + url)
    assert(valid_url(url))
    assert(valid_version(url))
    assert(path(url) == '/datasources?api-version=2020-06-30')

def test_list_skillsets():
    url = Urls().list_skillsets()
    print('url: ' + url)
    assert(valid_url(url))
    assert(valid_version(url))
    assert(path(url) == '/skillsets?api-version=2020-06-30')

def test_get_index():
    url = Urls().get_index('things')
    print('url: ' + url)
    assert(valid_url(url))
    assert(valid_version(url))
    assert(path(url) == '/indexes/things?api-version=2020-06-30')

def test_get_indexer():
    url = Urls().get_indexer('things')
    print('url: ' + url)
    assert(valid_url(url))
    assert(valid_version(url))
    assert(path(url) == '/indexers/things?api-version=2020-06-30')

def test_get_indexer_status():
    url = Urls().get_indexer_status('things')
    print('url: ' + url)
    assert(valid_url(url))
    assert(valid_version(url))
    assert(path(url) == '/indexers/things/status?api-version=2020-06-30')

def test_get_datasource():
    url = Urls().get_datasource('azureblob-documents')
    print('url: ' + url)
    assert(valid_url(url))
    assert(valid_version(url))
    assert(path(url) == '/datasources/azureblob-documents?api-version=2020-06-30')

def test_get_skillset():
    url = Urls().get_skillset('s1')
    print('url: ' + url)
    assert(valid_url(url))
    assert(valid_version(url))
    assert(path(url) == '/skillsets/s1?api-version=2020-06-30')

def test_create_index():
    url = Urls().create_index()
    print('url: ' + url)
    assert(valid_url(url))
    assert(valid_version(url))
    assert(path(url) == '/indexes?api-version=2020-06-30')

def test_modify_index():
    url = Urls().modify_index('documents')
    print('url: ' + url)
    assert(valid_url(url))
    assert(valid_version(url))
    assert(path(url) == '/indexes/documents?api-version=2020-06-30')

def test_create_indexer():
    url = Urls().create_indexer()
    print('url: ' + url)
    assert(valid_url(url))
    assert(valid_version(url))
    assert(path(url) == '/indexers?api-version=2020-06-30')

def test_modify_indexer():
    url = Urls().modify_indexer('documents')
    print('url: ' + url)
    assert(valid_url(url))
    assert(valid_version(url))
    assert(path(url) == '/indexers/documents?api-version=2020-06-30')

def test_reset_indexer():
    url = Urls().reset_indexer('documents')
    print('url: ' + url)
    assert(valid_url(url))
    assert(valid_version(url))
    assert(path(url) == '/indexers/documents/reset?api-version=2020-06-30')

def test_run_indexer():
    url = Urls().run_indexer('documents')
    print('url: ' + url)
    assert(valid_url(url))
    assert(valid_version(url))
    assert(path(url) == '/indexers/documents/run?api-version=2020-06-30')

def test_create_datasource():
    url = Urls().create_datasource()
    print('url: ' + url)
    assert(valid_url(url))
    assert(valid_version(url))
    assert(path(url) == '/datasources?api-version=2020-06-30')

def test_modify_datasource():
    url = Urls().modify_datasource('documents')
    print('url: ' + url)
    assert(valid_url(url))
    assert(valid_version(url))
    assert(path(url) == '/datasources/documents?api-version=2020-06-30')

def test_create_synmap():
    url = Urls().create_synmap()
    print('url: ' + url)
    assert(valid_url(url))
    assert(valid_version(url))
    assert(path(url) == '/synonymmaps?api-version=2020-06-30')

def test_modify_synmap():
    url = Urls().modify_synmap('s1')
    print('url: ' + url)
    assert(valid_url(url))
    assert(valid_version(url))
    assert(path(url) == '/synonymmaps/s1?api-version=2020-06-30')

def test_create_skillset():
    url = Urls().create_skillset()
    print('url: ' + url)
    assert(valid_url(url))
    assert(valid_version(url))
    assert(path(url) == '/skillsets?api-version=2020-06-30')

def test_modify_skillset():
    url = Urls().modify_skillset('skills1')
    print('url: ' + url)
    assert(valid_url(url))
    assert(valid_version(url))
    assert(path(url) == '/skillsets/skills1?api-version=2020-06-30')

def test_search_index():
    url = Urls().search_index('things')
    print('url: ' + url)
    assert(valid_url(url))
    assert(valid_version(url))
    assert(path(url) == '/indexes/things/docs/search?api-version=2020-06-30')

def test_lookup_doc():
    url = Urls().lookup_doc('things', 'x123')
    print('url: ' + url)
    assert(valid_url(url))
    assert(valid_version(url))
    assert(path(url) == '/indexes/things/docs/x123?api-version=2020-06-30')
