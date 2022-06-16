#!/bin/bash

# Bash shell that defines parameters and environment variables used 
# in this app, and is "sourced" by the other scripts in this repo.
# Chris Joakim, Microsoft, November 2021

export subscription=$AZURE_SUBSCRIPTION_ID
export user=$USER
export primary_region="eastus"
export primary_rg=$USER"search"

export storage_rg=$primary_rg
export storage_region=$primary_region
export storage_name=$primary_rg
export storage_kind="BlobStorage"     # {BlobStorage, BlockBlobStorage, FileStorage, Storage, StorageV2}]
export storage_sku="Standard_LRS"     # {Premium_LRS, Premium_ZRS, Standard_GRS, Standard_GZRS, , Standard_RAGRS, Standard_RAGZRS, Standard_ZRS]
export storage_access_tier="Hot"      # Cool, Hot

export search_rg=$primary_rg
export search_region=$primary_region
export search_name=$primary_rg
export search_sku="Standard"

export cogsvcs_rg=$primary_rg
export cogsvcs_region=$primary_region
export cogsvcs_name=$primary_rg
export cogsvcs_kind="CognitiveServices"
export cogsvcs_sku="S0"
