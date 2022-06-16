#!/bin/bash

# Bash and python script to wrangle the raw data files in the openflights/raw/
# directory into mongoimport files in the openflights/import_json/ directory.
# Users of this repo don't need to execute this script, as the output files
# are already present in the openflights/import_json/ directory.
# Chris Joakim, Microsoft, June 2021

mkdir -p tmp

echo 'airports ...'
python main.py parse_openflights_data airports  > openflights/import_json/airports.json
wc openflights/raw/airports.dat
wc openflights/import_json/airports.json

echo 'airlines ...'
python main.py parse_openflights_data airlines  > openflights/import_json/airlines.json
wc openflights/raw/airlines.dat
wc openflights/import_json/airlines.json

echo 'routes ...'
python main.py parse_openflights_data routes    > openflights/import_json/routes.json
wc openflights/raw/routes.dat
wc openflights/import_json/routes.json

echo 'planes ...'
python main.py parse_openflights_data planes    > openflights/import_json/planes.json
wc openflights/raw/planes.dat
wc openflights/import_json/planes.json

echo 'countries ...'
python main.py parse_openflights_data countries > openflights/import_json/countries.json
wc openflights/raw/countries.dat
wc openflights/import_json/countries.json

echo 'done'

# $ ./wrangle_openflights_data.sh
# airports ...
#     7699   26842 1127345 openflights/raw/airports.dat
#     7698   26832 2371746 openflights/import_json/airports.json
# airlines ...
#     6162   19307  396916 openflights/raw/airlines.dat
#     6161   19305  882618 openflights/import_json/airlines.json
# routes ...
#    67664   93256 2377277 openflights/raw/routes.dat
#    67663   93291 13542463 openflights/import_json/routes.json
# planes ...
#      247     677    8346 openflights/raw/planes.dat
#      246     672   14083 openflights/import_json/planes.json
# countries ...
#      262     392    6014 openflights/raw/countries.dat
#      261     391   14659 openflights/import_json/countries.json
# done
