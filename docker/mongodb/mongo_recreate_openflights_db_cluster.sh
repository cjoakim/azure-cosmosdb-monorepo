#!/bin/bash

# Bash script to execute the mongoimport program to load the reference database
# with the sample data provided in this repo.
# Chris Joakim, Microsoft, April 2022

echo 'init database ...'
mongo < mongo/openflights_init.ddl

echo 'sleeping 10 after init database...'
sleep 10

echo 'mongoimport airlines ...'
mongoimport \
    --db OpenFlights \
    --collection Airlines \
    --file openflights/import_json/airlines.json \
    --numInsertionWorkers 1 \
    --batchSize 24  # no --ssl

echo 'mongoimport airports ...'

mongoimport \
    --db OpenFlights \
    --collection Airports \
    --file openflights/import_json/airports.json \
    --numInsertionWorkers 1 \
    --batchSize 24  # no --ssl

echo 'mongoimport countries ...'
mongoimport \
    --db OpenFlights \
    --collection Countries \
    --file openflights/import_json/countries.json \
    --numInsertionWorkers 1 \
    --batchSize 24  # no --ssl

echo 'mongoimport planes ...'
mongoimport \
    --db OpenFlights \
    --collection Planes \
    --file openflights/import_json/planes.json \
    --numInsertionWorkers 1 \
    --batchSize 24  # no --ssl

echo 'mongoimport routes ...'
mongoimport \
    --db OpenFlights \
    --collection Routes \
    --file openflights/import_json/routes.json \
    --numInsertionWorkers 1 \
    --batchSize 24  # no --ssl

echo 'done'
