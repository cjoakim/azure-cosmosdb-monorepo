#!/bin/bash

# Bash script with AZ CLI to automate the creation/deletion of
# an Azure Cognitive Services account.
# Chris Joakim, Microsoft, November 2021
#
# Note: In order for this az provisioning script to work, your Azure account 
# must have a Cognitive Services Contributor role assigned.  The alternative
# solution is to simply provision the CognitiveServices account in Azure Portal.
# See https://docs.microsoft.com/en-us/azure/cognitive-services/cognitive-services-apis-create-account-cli?tabs=windows

# az login

source config.sh

arg_count=$#
processed=0

create() {
    processed=1
    echo 'creating cogsvcs rg: '$cogsvcs_rg
    az group create \
        --location $cogsvcs_region \
        --name $cogsvcs_rg \
        --subscription $subscription \
        > tmp/cogsvcs_rg_create.json

    echo 'creating cogsvcs account: '$cogsvcs_name
    az cognitiveservices account create \
        --name $cogsvcs_name \
        --resource-group $cogsvcs_rg \
        --location $cogsvcs_region \
        --kind $cogsvcs_kind \
        --sku $cogsvcs_sku \
        --yes \
        > tmp/cogsvcs_account_create.json

    sleep 10 

    info
}

info() {
    processed=1
    echo 'cogsvcs account show: '$cogsvcs_name
    az cognitiveservices account show \
        --name $cogsvcs_name \
        --resource-group $cogsvcs_rg \
        > tmp/cogsvcs_account_show.json

    echo 'cogsvcs account keys list: '$cogsvcs_name
    az cognitiveservices account keys list \
        --name $cogsvcs_name \
        --resource-group $cogsvcs_rg \
        > tmp/cogsvcs_keys_list.json
}

list_skus() {
    processed=1
    az cognitiveservices account list-skus > tmp/cognitiveservices_sku_list.json
}

display_usage() {
    echo 'Usage:'
    echo './cognitive.sh create'
    echo './cognitive.sh info'
    echo './cognitive.sh list_skus'
}

# ========== "main" logic below ==========

if [ $arg_count -gt 0 ]
then
    for arg in $@
    do
        if [ $arg == "create" ];    then create; fi 
        if [ $arg == "info" ];      then info; fi 
        if [ $arg == "list_skus" ]; then list_skus; fi 
    done
fi

if [ $processed -eq 0 ]; then display_usage; fi

echo 'done'
