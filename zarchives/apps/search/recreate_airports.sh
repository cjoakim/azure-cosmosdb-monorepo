#!/bin/bash

# Delete and recreate the airports index, and related objects, in Azure Cognitive Search.
# The datasource for this index is Azure CosmosDB.
# Chris Joakim, Microsoft, December 2021

source venv/bin/activate

# echo '=========='
# python cosmos.py load_airports dev airports no-duplicates
# sleep 5

echo '=========='
python search-client.py delete_indexer airports
sleep 5

echo '=========='
python search-client.py delete_index airports
sleep 5

echo '=========='
python search-client.py delete_datasource cosmosdb-dev-airports
sleep 5

echo '=========='
echo 'Tear-down steps complete, Recreating in 30-seconds...'
sleep 30

echo '=========='
python search-client.py create_cosmos_datasource dev airports
sleep 15

echo '=========='
python search-client.py create_index airports airports_index_v1
sleep 5

echo '=========='
python search-client.py create_indexer airports airports_indexer_v1
sleep 5

echo 'wait for the indexer to complete, then:'
echo 'python search-client.py search_index airports all'
