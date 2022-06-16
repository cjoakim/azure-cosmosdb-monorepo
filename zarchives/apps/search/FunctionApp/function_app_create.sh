#!/bin/bash

# Chris Joakim, Microsoft, November 2021

az functionapp create \
    --resource-group cjoakimsearch \
    --os-type Linux \
    --consumption-plan-location eastus \
    --runtime python \
    --runtime-version 3.9 \
    --functions-version 2 \
    --name cjoakimsearchapp \
    --storage-account cjoakimsearch

# Storage account 'cjoakimsearch' has no 'queue' endpoint. It must have table, queue, and blob endpoints all enabled
# Punted on this az cli script - created and deployed the Function with VSC instead.
