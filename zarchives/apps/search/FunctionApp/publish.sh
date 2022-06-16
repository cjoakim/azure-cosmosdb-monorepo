#!/bin/bash

# Deploy the Azure Function App containing the Custom Skill implementation.
# Chris Joakim, Microsoft, 2020/09/26

app_name="cjoakimsearchapp"

echo 'publishing function app named: '$app_name

func azure functionapp publish $app_name

echo 'done'

# Partial output below:
# ...
# Resetting all workers for cjoakimsearchapp.azurewebsites.net
# Deployment successful.
# Remote build succeeded!
# Syncing triggers...
# Functions in cjoakimsearchapp:
#     TopWordsSkill - [httpTrigger]
#         Invoke url: https://cjoakimsearchapp.azurewebsites.net/api/topwordsskill?code=...
