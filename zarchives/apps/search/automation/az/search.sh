#!/bin/bash

# Bash script with AZ CLI to automate the creation/deletion of an Azure Search account.
# Chris Joakim, Microsoft, November 2021
#
# See https://docs.microsoft.com/en-us/cli/azure/?view=azure-cli-latest

# az login

source config.sh

arg_count=$#
processed=0

delete() {
    processed=1
    echo 'deleting search rg: '$search_rg
    az group delete \
        --name $search_rg \
        --subscription $subscription \
        --yes \
        > tmp/search_rg_delete.json
}

create() {
    processed=1
    echo 'creating search rg: '$search_rg
    az group create \
        --location $search_region \
        --name $search_rg \
        --subscription $subscription \
        > tmp/search_rg_create.json

    echo 'creating search acct: '$search_name
    az search service create \
        --name $search_name \
        --resource-group $search_rg \
        --location $search_region \
        --sku $search_sku

    info
}

recreate() {
    processed=1
    delete
    create
    info 
}

info() {
    processed=1
    echo 'search acct show: '$search_name
    az search service show \
        --name $search_name \
        --resource-group $search_rg \
        --subscription $subscription \
        > tmp/search_acct_show.json
}

display_usage() {
    echo 'Usage:'
    echo './search.sh delete'
    echo './search.sh create'
    echo './search.sh recreate'
    echo './search.sh info'
}

# ========== "main" logic below ==========

if [ $arg_count -gt 0 ]
then
    for arg in $@
    do
        if [ $arg == "delete" ];   then delete; fi 
        if [ $arg == "create" ];   then create; fi 
        if [ $arg == "recreate" ]; then recreate; fi 
        if [ $arg == "info" ];     then info; fi 
    done
fi

if [ $processed -eq 0 ]; then display_usage; fi

echo 'done'
