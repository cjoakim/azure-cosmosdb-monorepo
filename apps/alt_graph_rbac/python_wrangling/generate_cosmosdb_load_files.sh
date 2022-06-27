#!/bin/bash

# Generate the several JSON files that CosmosDB/SQL API will be loaded with.
# Also scan the generated files and display their line counts.
# Chris Joakim, Microsoft, June 2022

echo 'data/load/*.* files ...'
rm data/load/*.*

echo 'generate_cosmosdb_load_files ...'
python main.py generate_cosmosdb_load_files

echo 'displaying the first two edge documents ...'
head -1 data/load/edges.json | jq
head -2 data/load/edges.json | tail -1 | jq

ls data/load/ | grep json$

echo 'scanning the generated load files ...'
python main.py scan_generated_cosmosdb_load_files

echo 'done'

# 32796 lines in file data/load/edges.json
# 247 lines in file data/load/azure_roles_map.json
# 245 lines in file data/load/azure_roles.json
# 453 lines in file data/load/azure_ad_permissions_map.json
# 85 lines in file data/load/azure_ad_roles_map.json
# 102 lines in file data/load/apps_map.json
# 415 lines in file data/load/azure_ad_roles.json
# 6105 lines in file data/load/azure_ad_permissions.json
# 300 lines in file data/load/application_roles.json
# 1100 lines in file data/load/people.json
# 100 lines in file data/load/apps.json
# 1073 lines in file data/load/people_map.json
# 43021 total lines in 12 json files
