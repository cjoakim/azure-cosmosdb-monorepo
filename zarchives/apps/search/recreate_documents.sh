#!/bin/bash

# Delete and recreate the documents index, and related objects, in Azure Cognitive Search.
# The datasource for this index is Azure Storage.
# Chris Joakim, Microsoft, November 2021

source venv/bin/activate

echo '=========='
#python search-client.py create_synmap synmap synonym_map_v1
python search-client.py update_synmap synmap synonym_map_v1
sleep 5

echo '=========='
python storage-client.py create_upload_list
sleep 5

echo '=========='
#python storage-client.py upload_files 999
sleep 5

echo '=========='
python search-client.py delete_indexer documents
sleep 5

echo '=========='
python search-client.py delete_skillset skillset
sleep 5

echo '=========='
python search-client.py delete_index documents
sleep 5

echo '=========='
python search-client.py delete_datasource azureblob-documents
sleep 5

echo '=========='
echo 'Tear-down steps complete, Recreating in 30-seconds...'
sleep 30

echo '=========='
python search-client.py create_blob_datasource documents
sleep 20

echo '=========='
python search-client.py create_index documents documents_index_v1
sleep 5

echo '=========='
python search-client.py create_skillset skillset skillset_v1
sleep 5

echo '=========='
python search-client.py create_indexer documents documents_indexer_v1
sleep 2

echo 'wait for the indexer to complete, then:'
echo 'python search-client.py search_index documents all'
