#!/bin/bash

# Bash script with AZ CLI to automate the creation an Azure IoT Hub and DPS.
# Chris Joakim, Microsoft, 2020/10/24
#
# See https://docs.microsoft.com/en-us/cli/azure/?view=azure-cli-latest

# az login
# az account set -s $AZURE_SUBSCRIPTION_ID
# az account show  (confirm that your expected Azure Subscription is shown)
# az extension add --name azure-iot  (see extensions.sh)

source ./provisioning_env.sh

arg_count=$#
processed=0

create() {
    processed=1
    echo 'creating rg: '$iothub_rg
    az group create \
        --location $iothub_region \
        --name $iothub_rg \
        --subscription $subscription \
        > out/iothub_rg_create.json

    echo 'creating hub: '$iothub_hub_name
    az iot hub create \
        --name $iothub_hub_name \
        --resource-group $iothub_rg \
        --location $iothub_region \
        --sku $iothub_hub_sku \
        --unit $iothub_hub_units \
        --partition-count $iothub_hub_partition_count \
        --subscription $subscription \
        > out/iothub_hub_create.json

    echo 'creating dps: '$iothub_dps_name
    az iot dps create \
        --name $iothub_dps_name \
        --resource-group $iothub_rg \
        --location $iothub_region \
        --sku $iothub_dps_sku \
        --unit $iothub_dps_units \
        --subscription $subscription \
        > out/iothub_dps_create.json
}

link_dps_to_hub() {
    processed=1
    source ./bash_env_export.sh
    echo $AZURE_IOTHUB_CONN_STR

    echo 'az iot hub show: '$iothub_hub_name
    az iot hub show \
        --name $iothub_hub_name \
        --resource-group $iothub_rg \
        --subscription $subscription \
        > out/iothub_hub_show.json

    echo 'az iot dps linked-hub create: '$iothub_dps_name
    az iot dps linked-hub create \
        --resource-group $iothub_rg \
        --dps-name $iothub_dps_name \
        --connection-string $AZURE_IOTHUB_CONN_STR \
        --location $iothub_region \
        > out/iothub_dps_link_create.json
}

info() {
    processed=1
    echo 'hub list: '$iothub_name
    az iot hub list \
        --resource-group $iothub_rg \
        > out/iothub_hub_list.json

    echo 'hub show: '$iothub_name
    az iot hub show \
        --name $iothub_hub_name \
        --resource-group $iothub_rg \
        --subscription $subscription \
        > out/iothub_hub_show.json

    echo 'hub show-connection-string: '$iothub_name
    az iot hub show-connection-string \
        --all \
        --name $iothub_hub_name \
        --resource-group $iothub_rg \
        --subscription $subscription \
        > out/iothub_hub_show_conn_str.json

    echo 'dps list in rg: '$iothub_rg
    az iot dps list \
        --resource-group $iothub_rg \
        > out/iothub_dps_list.json

    echo 'az iot dps linked-hub list: '$iothub_dps_name
    az iot dps linked-hub list \
        --dps-name $iothub_dps_name \
        --resource-group $iothub_rg \
        > out/iothub_linked_hub_list.json

    # these 3 commands from https://docs.microsoft.com/en-us/azure/iot-hub/quickstart-send-telemetry-python
    echo 'properties.eventHubEndpoints.events.endpoint for iothub '$iothub_hub_name
    az iot hub show --query properties.eventHubEndpoints.events.endpoint --name $iothub_hub_name

    echo 'properties.eventHubEndpoints.events.path for iothub '$iothub_hub_name
    az iot hub show --query properties.eventHubEndpoints.events.path --name $iothub_hub_name

    echo 'service policy primaryKey for iothub '$iothub_hub_name
    az iot hub policy show --name service --query primaryKey --hub-name $iothub_hub_name
}

register_device1() {
    processed=1
    echo 'az iot hub device-identity create: '$iothub_device_id1
    az iot hub device-identity create \
        --device-id $iothub_device_id1 \
        --hub-name $iothub_hub_name \
        --resource-group $iothub_rg \
        > out/iothub_device_id1_create.json

    echo 'az iot hub device-identity list in hub: '$iothub_hub_name
    az iot hub device-identity list \
        --hub-name $iothub_hub_name \
        > out/iothub_device_list.json

    echo 'az iot hub device-identity show: '$iothub_device_id1
    az iot hub device-identity show \
        --device-id $iothub_device_id1 \
        --hub-name $iothub_hub_name \
        --resource-group $iothub_rg \
        > out/iothub_device_id1_show.json

    echo 'az iot hub device-identity show-connection-string: '$iothub_device_id1
    az iot hub device-identity show-connection-string \
        --device-id $iothub_device_id1 \
        --hub-name $iothub_hub_name \
        --resource-group $iothub_rg \
        > out/iothub_device_id1_conn_str.json
}

register_device2() {
    processed=1
    echo 'az iot hub device-identity create: '$iothub_device_id2
    az iot hub device-identity create \
        --device-id $iothub_device_id2 \
        --hub-name $iothub_hub_name \
        --resource-group $iothub_rg \
        > out/iothub_device_id2_create.json

    echo 'az iot hub device-identity list in hub: '$iothub_hub_name
    az iot hub device-identity list \
        --hub-name $iothub_hub_name \
        > out/iothub_device_list.json

    echo 'az iot hub device-identity show: '$iothub_device_id2
    az iot hub device-identity show \
        --device-id $iothub_device_id2 \
        --hub-name $iothub_hub_name \
        --resource-group $iothub_rg \
        > out/iothub_device_id2_show.json

    echo 'az iot hub device-identity show-connection-string: '$iothub_device_id2
    az iot hub device-identity show-connection-string \
        --device-id $iothub_device_id2 \
        --hub-name $iothub_hub_name \
        --resource-group $iothub_rg \
        > out/iothub_device_id2_conn_str.json
}

pause() {
    echo 'pause/sleep 60...'
    sleep 60
}

display_usage() {
    echo 'Usage:'
    echo './iothub.sh create'
    echo './iothub.sh link_dps_to_hub'
    echo './iothub.sh info'
    echo './iothub.sh register_device1'
    echo './iothub.sh register_device2'
}

# ========== "main" logic below ==========

if [ $arg_count -gt 0 ]
then
    for arg in $@
    do
        if [ $arg == "create" ]; then create; fi 
        if [ $arg == "info" ];   then info; fi 

        if [ $arg == "link_dps_to_hub" ];  then link_dps_to_hub; fi 
        if [ $arg == "register_device1" ]; then register_device1; fi 
        if [ $arg == "register_device2" ]; then register_device2; fi 
    done
fi

if [ $processed -eq 0 ]; then display_usage; fi

echo 'done'
