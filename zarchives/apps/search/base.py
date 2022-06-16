"""
This is the superclass of classes StorageClient and SearchHttpClient
in this directory.
"""

__author__  = 'Chris Joakim'
__email__   = "chjoakim@microsoft.com"
__license__ = "MIT"
__version__ = "November 2021"

import json
import os
import sys
import time


class BaseClass:
    """
    This is the abstract superclass of the several classes in this project -
    SearchClient, StorageClient, CosmosClient, Schemas, Urls.
    """

    def __init__(self):
        self.stor_acct_name = os.environ['AZURE_SEARCH_STORAGE_ACCOUNT']
        self.stor_acct_key  = os.environ['AZURE_SEARCH_STORAGE_KEY']
        self.stor_acct_conn_str = os.environ['AZURE_SEARCH_STORAGE_CONNECTION_STRING']
        self.blob_container  = 'documents'
        self.blob_svc_client = None

    def epoch(self):
        return time.time()

    def blob_datasource_name(self, container):
        return 'azureblob-{}'.format(container)

    def cosmos_datasource_name(self, dbname, container):
        return 'cosmosdb-{}-{}'.format(dbname, container)

    def cosmos_datasource_name_conn_str(self, dbname):
        # This method depends on these two environment variables that look like this; see Azure Portal.
        acct = os.environ['AZURE_COSMOSDB_SQLDB_ACCT']
        key  = os.environ['AZURE_COSMOSDB_SQLDB_KEY']
        return 'AccountEndpoint=https://{}.documents.azure.com;AccountKey={};Database={}'.format(acct, key, dbname)

    def read_text_file(self, infile):
        lines = list()
        with open(infile, 'rt') as f:
            for idx, line in enumerate(f):
                lines.append(line.strip())
        return lines

    def load_json_file(self, infile):
        with open(infile, 'rt') as json_file:
            return json.loads(str(json_file.read()))

    def write_json_file(self, obj, outfile):
        with open(outfile, 'wt') as f:
            f.write(json.dumps(obj, sort_keys=False, indent=2))
            print('file written: {}'.format(outfile))
