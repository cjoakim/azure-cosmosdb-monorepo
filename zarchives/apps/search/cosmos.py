"""
Usage:
    python cosmos.py load_airports dev airports duplicates
    python cosmos.py load_airports dev airports no-duplicates
"""

__author__  = 'Chris Joakim'
__email__   = "chjoakim@microsoft.com"
__license__ = "MIT"
__version__ = "December 2021"

import json
import os
import pprint
import sys
import time
import uuid

import arrow

import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.errors as errors
import azure.cosmos.http_constants as http_constants
import azure.cosmos.diagnostics as diagnostics
import azure.cosmos.documents as documents
import azure.cosmos.exceptions as exceptions
import azure.cosmos.partition_key as partition_key

from docopt import docopt

from base import BaseClass


class CosmosClient(BaseClass):
    """
    This class is executed from the command line to upload documents to Azure CosmosDB
    for indexing by Azure Cognitive Search.
    """

    def __init__(self):
        url = os.environ['AZURE_COSMOSDB_SQLDB_URI']
        key = os.environ['AZURE_COSMOSDB_SQLDB_KEY']
        self.cosmos_client = cosmos_client.CosmosClient(url, {'masterKey': key})
        print('cosmos_client: {}'.format(self.cosmos_client))

    def load_airports(self, dbname, cname, duplicates_ind):
        print('load_airports: {} {}'.format(dbname, cname))
        upsert_count = 0
        try:
            db_client = self.cosmos_client.get_database_client(dbname)
            print('db_client: {}'.format(db_client))
            container_client = db_client.get_container_client(cname)
            print('container_client: {}'.format(container_client))

            airports_array = self.load_json_file('data/us_airports.json')
            for idx, item in enumerate(airports_array):
                item['epoch'] = self.epoch()
                item['note'] = 'loaded by python client {}'.format(str(arrow.now()))
                if duplicates_ind == 'no-duplicates':
                    # retain the 'id' value already present in the item
                    pass  
                else:
                    # Generate a random UUID so that a new document will be created
                    item['id'] = str(uuid.uuid4())
                try:
                    pk = item['pk'].strip()
                    if len(pk) == 3:
                        print("upserting item {}:\n{}".format(idx, item))
                        container_client.upsert_item(item)
                        upsert_count = upsert_count + 1
                    else:
                        print("bypassing item {} due to pk:\n{}".format(idx, item))
                except Exception as e2:
                    print('exception on doc: {}'.format(item))
                    print(e2)
        except Exception as e1:
            print('exception in load_airports')
            print(e1)

        print('airports array count:   {}'.format(len(airports_array)))    
        print('document upsert count:  {}'.format(upsert_count))


def print_options(msg):
    print(msg)
    arguments = docopt(__doc__, version=__version__)
    print(arguments)


if __name__ == "__main__":

    if len(sys.argv) > 1:
        func = sys.argv[1].lower()
        print('func: {}'.format(func))
        client = CosmosClient()

        if func == 'load_airports':
            dbname = sys.argv[2]
            container = sys.argv[3]
            duplicates_ind = sys.argv[4]
            client.load_airports(dbname, container, duplicates_ind)
        else:
            print_options('Error: invalid function: {}'.format(func))
    else:
        print_options('Error: no function argument provided.')
