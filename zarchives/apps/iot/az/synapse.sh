#!/bin/bash

# Bash script with AZ CLI to automate the creation/deletion of my
# Azure DataLake Gen2 account (a storage account, really).
# Chris Joakim, Microsoft, 2020/10/24
#
# https://docs.microsoft.com/en-us/azure/synapse-analytics/quickstart-create-workspace
# https://docs.microsoft.com/en-us/azure/cosmos-db/configure-synapse-link
# https://docs.microsoft.com/en-us/azure/synapse-analytics/sql-data-warehouse/sql-data-warehouse-manage-compute-overview
#
# az extension add -n storage-preview
# az extension add --name synapse


# az login

source ./provisioning_env.sh

arg_count=$#
processed=0


create() {
    processed=1
    az extension add --name synapse

    echo 'creating synapse rg: '$synapse_rg
    az group create \
        --location $synapse_region \
        --name $synapse_rg \
        --subscription $subscription \
        > out/synapse_rg_create.json

    echo 'creating synapse storage acct: '$synapse_name
    az storage account create \
        --name $synapse_name \
        --resource-group $synapse_rg \
        --location $synapse_region \
        --kind $storage_kind \
        --access-tier $synapse_stor_access_tier \
        --hierarchical-namespace true \
        --sku $synapse_stor_sku \
        --subscription $subscription \
        > out/synapse_storage_acct_create.json

    pause

    storage_name=$synapse_name

    echo 'creating synapse workspace: '$synapse_name' with storage: '$storage_name
    az synapse workspace create \
        --name $synapse_name \
        --resource-group $synapse_rg \
        --storage-account $synapse_name \
        --file-system $synapse_fs_name \
        --sql-admin-login-user $AZURE_SYNAPSE_USER \
        --sql-admin-login-password $AZURE_SYNAPSE_PASS \
        --location $synapse_region \
        --debug \
        > out/synapse_workspace_create.json

    pause

    echo 'creating synapse workspace firewall-rule'
    az synapse workspace firewall-rule create \
        --name allowAll \
        --workspace-name $synapse_name \
        --resource-group $synapse_rg \
        --start-ip-address 0.0.0.0 \
        --end-ip-address 255.255.255.255  \
        > out/synapse_firewall_rule_create.json
}

create_spark_pool() {
    processed=1
    echo 'az synapse spark pool create: '$synapse_spark_pool_name
    az synapse spark pool create \
        --name $synapse_spark_pool_name \
        --workspace-name $synapse_name \
        --resource-group $synapse_rg \
        --spark-version 2.4 \
        --enable-auto-pause true \
        --delay 120 \
        --node-count $synapse_spark_pool_count \
        --node-size $synapse_spark_pool_size \
        > out/synapse_spark_pool_create.json
}

create_sql_pool() {
    processed=1
    echo 'az synapse sql pool create: '$synapse_sql_pool_name', perf: '$synapse_sql_pool_perf
    az synapse sql pool create \
        --name $synapse_sql_pool_name  \
        --performance-level $synapse_sql_pool_perf \
        --workspace-name $synapse_name \
        --resource-group $synapse_rg \
        > out/synapse_sql_pool_create.json
}

info() {
    processed=1
    echo 'az storage acct show: '$synapse_name
    az storage account show \
        --name $synapse_name \
        --resource-group $synapse_rg \
        --subscription $subscription \
        > out/synapse_storage_acct_show.json

    echo 'az storage acct keys: '$synapse_name
    az storage account keys list \
        --account-name $synapse_name \
        --resource-group $synapse_rg \
        --subscription $subscription \
        > out/synapse_storage_acct_keys.json

    echo 'az synapse workspace list:'
    az synapse workspace list \
        > out/synapse_workspace_list.json

    echo 'synapse acct show: '$synapse_name
    az synapse workspace show \
        --name $synapse_name \
        --resource-group $synapse_rg \
        > out/synapse_acct_show.json

    echo 'az synapse sql pool list: '$synapse_name
    az synapse sql pool list \
        --resource-group $synapse_rg \
        --workspace-name $synapse_name \
        > out/synapse_sql_pool_list.json

    echo 'az synapse spark pool list: '$synapse_name
    az synapse spark pool list \
        --resource-group $synapse_rg \
        --workspace-name $synapse_name \
        > out/synapse_spark_pool_list.json

    echo 'az synapse sql pool show: '$synapse_sql_pool_name
    az synapse sql pool show \
        --name $synapse_sql_pool_name \
        --resource-group $synapse_rg \
        --workspace-name $synapse_name \
        > out/synapse_sql_pool_show.json

    echo 'az synapse spark pool show: '$synapse_spark_pool_name
    az synapse spark pool show \
        --name $synapse_spark_pool_name \
        --resource-group $synapse_rg \
        --workspace-name $synapse_name \
        > out/synapse_spark_pool_show.json
}

pause() {
    echo 'pause/sleep 60...'
    sleep 60
}

adhoc() {
    processed=1
    echo 'az synapse spark pool create: '$synapse_spark_pool_name
    az synapse spark pool create \
        --name $synapse_spark_pool_name \
        --workspace-name $synapse_name \
        --resource-group $synapse_rg \
        --spark-version 2.4 \
        --node-count $synapse_spark_pool_count \
        --node-size $synapse_spark_pool_size \
        > out/synapse_spark_pool_create.json

        # --enable-auto-pause true \
        # --delay 120 \

    echo 'az synapse sql pool create: '$synapse_sql_pool_name', perf: '$synapse_sql_pool_perf
    az synapse sql pool create \
        --name $synapse_sql_pool_name  \
        --performance-level $synapse_sql_pool_perf \
        --workspace-name $synapse_name \
        --resource-group $synapse_rg \
        > out/synapse_sql_pool_create.json
}

display_usage() {
    echo 'Usage:'
    echo './synapse.sh delete'
    echo './synapse.sh create'
    echo './synapse.sh create_spark_pool'
    echo './synapse.sh create_sql_pool'
    echo './synapse.sh info'
    echo './synapse.sh create pause create_spark_pool pause create_sql_pool pause info'
    echo './synapse.sh create pause info pause create_spark_pool pause info'
    echo './synapse.sh create_sql_pool pause info'
}

# ========== "main" logic below ==========

date 

if [ $arg_count -gt 0 ]
then
    for arg in $@
    do
        if [ $arg == "delete" ];            then delete; fi 
        if [ $arg == "create" ];            then create; fi 
        if [ $arg == "create_spark_pool" ]; then create_spark_pool; fi 
        if [ $arg == "create_sql_pool" ];   then create_sql_pool; fi
        if [ $arg == "info" ];              then info; fi 
        if [ $arg == "pause" ];             then pause; fi 
    done
fi

if [ $processed -eq 0 ]; then display_usage; fi

date 
echo 'done'
