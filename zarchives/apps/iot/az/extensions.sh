#!/bin/bash

# Bash script to install the several az CLI extensions for this project.
# Chris Joakim, Microsoft, 2020/10/24

# az login

source ./provisioning_env.sh

arg_count=$#
processed=0

list() {
    processed=1
    echo 'listing available az cli extensions ...'
    az extension list-available --output table

    echo 'listing installed az cli extensions ...'
    az extension list --output table
}

install() {
    processed=1
    echo 'adding storage-preview extension ...'
    az extension add -n storage-preview

    echo 'adding stream-analytics extension ...'
    az extension add -n stream-analytics

    echo 'adding azure-iot extension ...'
    az extension add --name azure-iot

    echo 'adding synapse extension ...'
    az extension add --name synapse
}

display_usage() {
    echo 'Usage:'
    echo './extensions.sh list'
    echo './extensions.sh install'
}

# ========== "main" logic below ==========

if [ $arg_count -gt 0 ]
then
    for arg in $@
    do
        if [ $arg == "list" ];    then list; fi 
        if [ $arg == "install" ]; then install; fi 
    done
fi

if [ $processed -eq 0 ]; then display_usage; fi

echo 'done'



# Output below:
#
# $ ./extensions.sh list
# listing available az cli extensions ...
# Name                            Version    Summary                                                                                                            Preview    Experimental    Installed
# ------------------------------  ---------  -----------------------------------------------------------------------------------------------------------------  ---------  --------------  ------------------------
# account                         0.1.0      Microsoft Azure Command-Line Tools SubscriptionClient Extension                                                    False      True            False
# aem                             0.1.1      Manage Azure Enhanced Monitoring Extensions for SAP                                                                False      False           False
# ai-did-you-mean-this            0.2.1      Recommend recovery options on failure.                                                                             False      True            False
# ai-examples                     0.2.2      Add AI powered examples to help content.                                                                           True       False           False
# aks-preview                     0.4.57     Provides a preview for upcoming AKS features                                                                       True       False           False
# alertsmanagement                0.1.0      Microsoft Azure Command-Line Tools Alerts Extension                                                                False      True            False
# alias                           0.5.2      Support for command aliases                                                                                        True       False           False
# application-insights            0.1.9      Support for managing Application Insights components and querying metrics, events, and logs from such components.  True       False           False
# azure-batch-cli-extensions      6.0.0      Additional commands for working with Azure Batch service                                                           False      False           False
# azure-cli-iot-ext               0.8.9      The Azure IoT extension for Azure CLI.                                                                             False      False           False
# azure-cli-ml                    1.10.0     Microsoft Azure Command-Line Tools AzureML Command Module                                                          False      False           False
# azure-devops                    0.18.0     Tools for managing Azure DevOps.                                                                                   False      False           False
# azure-firewall                  0.5.0      Manage Azure Firewall resources.                                                                                   True       False           False
# azure-iot                       0.9.7      The Azure IoT extension for Azure CLI.                                                                             False      False           True (upgrade available)
# blockchain                      0.1.0      Microsoft Azure Command-Line Tools BlockchainManagementClient Extension                                            False      True            False
# blueprint                       0.1.1      Microsoft Azure Command-Line Tools Blueprint Extension                                                             False      True            False
# codespaces                      0.3.0      The Azure CLI Codespaces extension                                                                                 True       False           False
# connectedk8s                    0.2.1      Microsoft Azure Command-Line Tools Connectedk8s Extension                                                          True       False           False
# connectedmachine                0.1.1      Microsoft Azure Command-Line Tools Connectedmachine Extension                                                      True       False           False
# costmanagement                  0.1.0      Microsoft Azure Command-Line Tools CostManagementClient Extension                                                  False      True            False
# csvmware                        0.3.0      Manage Azure VMware Solution by CloudSimple.                                                                       True       False           False
# custom-providers                0.1.0      Microsoft Azure Command-Line Tools Custom Providers Extension                                                      False      True            False
# databox                         0.1.0      Microsoft Azure Command-Line Tools DataBox Extension                                                               False      True            False
# databricks                      0.4.0      Microsoft Azure Command-Line Tools DatabricksClient Extension                                                      True       False           False
# datafactory                     0.1.0      Microsoft Azure Command-Line Tools DataFactoryManagementClient Extension                                           False      True            False
# datashare                       0.1.0      Microsoft Azure Command-Line Tools DataShareManagementClient Extension                                             False      True            False
# db-up                           0.1.15     Additional commands to simplify Azure Database workflows.                                                          True       False           False
# deploy-to-azure                 0.2.0      Deploy to Azure using Github Actions.                                                                              True       False           False
# desktopvirtualization           0.1.0      Microsoft Azure Command-Line Tools DesktopVirtualizationAPIClient Extension                                        False      True            False
# dev-spaces                      1.0.5      Dev Spaces provides a rapid, iterative Kubernetes development experience for teams.                                False      False           False
# dms-preview                     0.11.0     Support for new Database Migration Service scenarios.                                                              True       False           False
# eventgrid                       0.4.9      Microsoft Azure Command-Line Tools EventGrid Command Module.                                                       True       False           False
# express-route                   0.1.3      Manage ExpressRoutes with preview features.                                                                        True       False           False
# express-route-cross-connection  0.1.1      Manage customer ExpressRoute circuits using an ExpressRoute cross-connection.                                      False      False           False
# front-door                      1.0.8      Manage networking Front Doors.                                                                                     False      False           False
# hack                            0.4.2      Microsoft Azure Command-Line Tools Hack Extension                                                                  True       False           False
# hardware-security-modules       0.1.0      Microsoft Azure Command-Line Tools AzureDedicatedHSMResourceProvider Extension                                     False      True            False
# healthcareapis                  0.2.0      Microsoft Azure Command-Line Tools HealthcareApisManagementClient Extension                                        False      False           False
# hpc-cache                       0.1.0      Microsoft Azure Command-Line Tools StorageCache Extension                                                          True       True            False
# image-copy-extension            0.2.6      Support for copying managed vm images between regions                                                              False      False           False
# import-export                   0.1.1      Microsoft Azure Command-Line Tools StorageImportExport Extension                                                   False      True            False
# interactive                     0.4.4      Microsoft Azure Command-Line Interactive Shell                                                                     True       False           False
# internet-analyzer               0.1.0rc5   Microsoft Azure Command-Line Tools Internet Analyzer Extension                                                     True       False           False
# ip-group                        0.1.2      Microsoft Azure Command-Line Tools IpGroup Extension                                                               True       False           False
# k8sconfiguration                0.1.8      Microsoft Azure Command-Line Tools K8sconfiguration Extension                                                      True       False           False
# keyvault-preview                0.1.3      Preview Azure Key Vault commands.                                                                                  True       False           False
# kusto                           0.1.0      Microsoft Azure Command-Line Tools KustoManagementClient Extension                                                 False      True            False
# log-analytics                   0.2.1      Support for Azure Log Analytics query capabilities.                                                                True       False           False
# log-analytics-solution          0.1.1      Support for Azure Log Analytics Solution                                                                           False      True            False
# logic                           0.1.0      Microsoft Azure Command-Line Tools LogicManagementClient Extension                                                 False      True            False
# maintenance                     1.0.1      Support for Azure maintenance management.                                                                          False      False           False
# managementpartner               0.1.3      Support for Management Partner preview                                                                             False      False           False
# mesh                            0.10.6     Support for Microsoft Azure Service Fabric Mesh - Public Preview                                                   True       False           False
# mixed-reality                   0.0.2      Mixed Reality Azure CLI Extension.                                                                                 True       False           False
# netappfiles-preview             0.3.2      Provides a preview for upcoming Azure NetApp Files (ANF) features.                                                 True       False           False
# notification-hub                0.2.0      Microsoft Azure Command-Line Tools Notification Hub Extension                                                      False      True            False
# peering                         0.2.0      Microsoft Azure Command-Line Tools PeeringManagementClient Extension                                               False      True            False
# portal                          0.1.1      Microsoft Azure Command-Line Tools Portal Extension                                                                False      True            False
# powerbidedicated                0.1.1      Microsoft Azure Command-Line Tools PowerBIDedicated Extension                                                      True       False           False
# privatedns                      0.1.1      Commands to manage Private DNS Zones                                                                               True       False           False
# resource-graph                  1.1.0      Support for querying Azure resources with Resource Graph.                                                          True       False           False
# sap-hana                        0.6.4      Additional commands for working with SAP HanaOnAzure instances.                                                    False      False           False
# spring-cloud                    0.3.1      Microsoft Azure Command-Line Tools spring-cloud Extension                                                          True       False           False
# storage-or-preview              0.4.0      Microsoft Azure Command-Line Tools Storage-ors-preview Extension                                                   True       False           False
# storage-preview                 0.2.11     Provides a preview for upcoming storage features.                                                                  True       False           True (upgrade available)
# storagesync                     0.1.0      Microsoft Azure Command-Line Tools MicrosoftStorageSync Extension                                                  False      True            False
# stream-analytics                0.1.0      Microsoft Azure Command-Line Tools stream-analytics Extension                                                      False      True            True
# subscription                    0.1.4      Support for subscription management preview.                                                                       True       False           False
# support                         1.0.2      Microsoft Azure Command-Line Tools Support Extension                                                               False      False           False
# synapse                         0.3.0      Microsoft Azure Command-Line Tools Synapse Extension                                                               True       False           True (upgrade available)
# timeseriesinsights              0.1.2      Microsoft Azure Command-Line Tools TimeSeriesInsightsClient Extension                                              False      True            False
# virtual-network-tap             0.1.0      Manage virtual network taps (VTAP).                                                                                True       False           False
# virtual-wan                     0.1.3      Manage virtual WAN, hubs, VPN gateways and VPN sites.                                                              True       False           False
# vm-repair                       0.3.1      Auto repair commands to fix VMs.                                                                                   False      False           False
# vmware                          0.6.0      Preview Azure VMware Solution commands.                                                                            True       False           False
# webapp                          0.2.24     Additional commands for Azure AppService.                                                                          True       False           False
# listing installed az cli extensions ...
# Experimental    ExtensionType    Name              Path                                                  Preview    Version
# --------------  ---------------  ----------------  ----------------------------------------------------  ---------  ---------
# False           whl              azure-iot         /Users/cjoakim/.azure/cliextensions/azure-iot         False      0.9.4
# True            whl              stream-analytics  /Users/cjoakim/.azure/cliextensions/stream-analytics  False      0.1.0
# False           whl              storage-preview   /Users/cjoakim/.azure/cliextensions/storage-preview   True       0.2.10
# False           whl              synapse           /Users/cjoakim/.azure/cliextensions/synapse           True       0.2.0
# done