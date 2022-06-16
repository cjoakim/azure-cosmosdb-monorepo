# Provisioning Azure Resources

To provision the Azure Resources for this example, see the **provision_all.sh** bash script 
in the **az/** directory of this repo.  

This script uses the [Azure Command-Line Interface (CLI)](https://docs.microsoft.com/en-us/cli/azure/) to provision the Azure PaaS service resources.  These **az CLI commands** are platform neutral - the exact same syntax is implemented for Windows, Linux, and macOS.
The **provision_all.sh** can easily be adapted to Window PowerShell.

Also see the **provision_env.sh** bash script in the **az/** directory of this repo.
This is used to set environment variables which are used by the other provisioning
bash scripts.  **Edit file provision_env.sh as necessary for your Azure Subscription**.
