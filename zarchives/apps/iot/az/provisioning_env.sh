#!/bin/bash

# Bash shell that defines parameters and environment variables used in provisioning the
# resources in this IoT project, and is "sourced" by the other scripts in this project.
# Chris Joakim, Microsoft, 2021/05/07

# environment variables for provisioning:

export subscription=$AZURE_SUBSCRIPTION_ID
export user=$USER
export primary_region="eastus"
export primary_rg="cjoakim-iot-cosmosdb-synapse"
#
export cosmos_sql_region=$primary_region
export cosmos_sql_rg=$primary_rg
export cosmos_sql_acct_name="cjoakimiotcosmossql"
export cosmos_sql_acct_consistency="Session"    # {BoundedStaleness, ConsistentPrefix, Eventual, Session, Strong}
export cosmos_sql_acct_kind="GlobalDocumentDB"  # {GlobalDocumentDB, MongoDB, Parse}
export cosmos_sql_dbname="dev"
export cosmos_sql_events_collname="events"
export cosmos_sql_events_pk="/pk"
export cosmos_sql_events_ru="1000"
#
export iothub_region=$primary_region
export iothub_rg=$primary_rg
export iothub_hub_name="cjoakimiotiothub"
export iothub_hub_sku="S1"
export iothub_hub_units="1"
export iothub_hub_partition_count="2"
#
# See file out/iothub_hub_show_conn_str.json, find SharedAccessKeyName=iothubowner
export iothub_hub_conn_string="HostName=cjoakimiotiothub.azure-devices.net;SharedAccessKeyName=iothubowner;SharedAccessKey=xcLH1OuSYxsaZ1JQGbMR+sAuHPnXc1Qtt5dEXTB+fys="
export iothub_dps_name="cjoakimiotiothubdps"
export iothub_dps_sku="S1"
export iothub_dps_units="1"

export iothub_device_id1="cjiothubdevice1"    # <-- non-edge device
export iothub_device_id2="cjiothubdevice2"    # <-- non-edge device
export iothub_device_edge1="cjiotedgedevice1" # <-- edge device, created with --edge-enabled flag
export iothub_device_edge2="cjiotedgedevice2" # <-- edge device, created with --edge-enabled flag

export iotedge_device1_dns_prefix="cjoakim-edge-uvm1"
export iotedge_device1_admin_user="cjoakim"
export iotedge_device1_admin_pass="xxxxxx"
export iotedge_device1_conn_str="HostName=cjoakimiotiothub.azure-devices.net;DeviceId=edge-vm1;SharedAccessKey=HsXFpZWN6JVMzDlzkb2UTpspQjd2ia3PLI591g1oZGg="
# export iotedge_device_deployment_template_url1="https://aka.ms/iotedge-vm-deploy"
# export iotedge_device_deployment_template_url2="https://raw.githubusercontent.com/Azure/iotedge-v-deploy/master/edgeDeploy.json"

# export iotedge_device_vm_name="vm-li37a3pukf72q"
# export iotedge_device_vm_ip="40.114.29.100"

#
export storage_region=$primary_region
export storage_rg=$primary_rg
export storage_name="cjoakimiotstor"
export storage_kind="BlobStorage"     # {BlobStorage, BlockBlobStorage, FileStorage, Storage, StorageV2}]
export storage_sku="Standard_LRS"     # {Premium_LRS, Premium_ZRS, Standard_GRS, Standard_GZRS, , Standard_RAGRS, Standard_RAGZRS, Standard_ZRS]
export storage_access_tier="Hot"      # Cool, Hot

export stream_analytics_region=$primary_region
export stream_analytics_rg=$primary_rg
export stream_analytics_name="cjoakimiotsa"

export synapse_region=$primary_region
export synapse_rg=$primary_rg
export synapse_name="cjoakimiotsynapse"
export synapse_stor_kind="StorageV2"       # {BlobStorage, BlockBlobStorage, FileStorage, Storage, StorageV2}]
export synapse_stor_sku="Standard_LRS"     # {Premium_LRS, Premium_ZRS, Standard_GRS, Standard_GZRS, , Standard_RAGRS, Standard_RAGZRS, Standard_ZRS]
export synapse_stor_access_tier="Hot"      # Cool, Hot
export synapse_admin_user=$AZURE_SYNAPSE_USER   # Use the system environment variable
export synapse_admin_pass=$AZURE_SYNAPSE_PASS   # Use the system environment variable
export synapse_fs_name="synapse_acct"
export synapse_sql_pool_name="cjdw200"
export synapse_sql_pool_perf="DW200c" 
export synapse_spark_pool_name="cjspark3s"
export synapse_spark_pool_count="3"
export synapse_spark_pool_size="Small"
