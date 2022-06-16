#!/bin/bash

# Execute the generated matrix of specifications.
# Chris Joakim, Microsoft, 2020-11-08


echo 'executing cost spec 1-standard-single-1-azone-3gb.txt ...'
dotnet run spec_matrix/1-standard-single-1-azone-3gb.txt > spec_matrix/out/1-standard-single-1-azone-3gb.json

echo 'executing cost spec 2-standard-single-1-azone-300gb.txt ...'
dotnet run spec_matrix/2-standard-single-1-azone-300gb.txt > spec_matrix/out/2-standard-single-1-azone-300gb.json

echo 'executing cost spec 3-standard-single-1-azone-30000gb.txt ...'
dotnet run spec_matrix/3-standard-single-1-azone-30000gb.txt > spec_matrix/out/3-standard-single-1-azone-30000gb.json

echo 'executing cost spec 4-standard-single-1-noazone-3gb.txt ...'
dotnet run spec_matrix/4-standard-single-1-noazone-3gb.txt > spec_matrix/out/4-standard-single-1-noazone-3gb.json

echo 'executing cost spec 5-standard-single-1-noazone-300gb.txt ...'
dotnet run spec_matrix/5-standard-single-1-noazone-300gb.txt > spec_matrix/out/5-standard-single-1-noazone-300gb.json

echo 'executing cost spec 6-standard-single-1-noazone-30000gb.txt ...'
dotnet run spec_matrix/6-standard-single-1-noazone-30000gb.txt > spec_matrix/out/6-standard-single-1-noazone-30000gb.json

echo 'executing cost spec 7-standard-multi-region-3-noazone-3gb.txt ...'
dotnet run spec_matrix/7-standard-multi-region-3-noazone-3gb.txt > spec_matrix/out/7-standard-multi-region-3-noazone-3gb.json

echo 'executing cost spec 8-standard-multi-region-3-noazone-300gb.txt ...'
dotnet run spec_matrix/8-standard-multi-region-3-noazone-300gb.txt > spec_matrix/out/8-standard-multi-region-3-noazone-300gb.json

echo 'executing cost spec 9-standard-multi-region-3-noazone-30000gb.txt ...'
dotnet run spec_matrix/9-standard-multi-region-3-noazone-30000gb.txt > spec_matrix/out/9-standard-multi-region-3-noazone-30000gb.json

echo 'executing cost spec 10-standard-multi-master-3-azone-3gb.txt ...'
dotnet run spec_matrix/10-standard-multi-master-3-azone-3gb.txt > spec_matrix/out/10-standard-multi-master-3-azone-3gb.json

echo 'executing cost spec 11-standard-multi-master-3-azone-300gb.txt ...'
dotnet run spec_matrix/11-standard-multi-master-3-azone-300gb.txt > spec_matrix/out/11-standard-multi-master-3-azone-300gb.json

echo 'executing cost spec 12-standard-multi-master-3-azone-30000gb.txt ...'
dotnet run spec_matrix/12-standard-multi-master-3-azone-30000gb.txt > spec_matrix/out/12-standard-multi-master-3-azone-30000gb.json

echo 'executing cost spec 13-standard-multi-master-3-noazone-3gb.txt ...'
dotnet run spec_matrix/13-standard-multi-master-3-noazone-3gb.txt > spec_matrix/out/13-standard-multi-master-3-noazone-3gb.json

echo 'executing cost spec 14-standard-multi-master-3-noazone-300gb.txt ...'
dotnet run spec_matrix/14-standard-multi-master-3-noazone-300gb.txt > spec_matrix/out/14-standard-multi-master-3-noazone-300gb.json

echo 'executing cost spec 15-standard-multi-master-3-noazone-30000gb.txt ...'
dotnet run spec_matrix/15-standard-multi-master-3-noazone-30000gb.txt > spec_matrix/out/15-standard-multi-master-3-noazone-30000gb.json

echo 'executing cost spec 16-autoscale-single-1-azone-3gb.txt ...'
dotnet run spec_matrix/16-autoscale-single-1-azone-3gb.txt > spec_matrix/out/16-autoscale-single-1-azone-3gb.json

echo 'executing cost spec 17-autoscale-single-1-azone-300gb.txt ...'
dotnet run spec_matrix/17-autoscale-single-1-azone-300gb.txt > spec_matrix/out/17-autoscale-single-1-azone-300gb.json

echo 'executing cost spec 18-autoscale-single-1-azone-30000gb.txt ...'
dotnet run spec_matrix/18-autoscale-single-1-azone-30000gb.txt > spec_matrix/out/18-autoscale-single-1-azone-30000gb.json

echo 'executing cost spec 19-autoscale-single-1-noazone-3gb.txt ...'
dotnet run spec_matrix/19-autoscale-single-1-noazone-3gb.txt > spec_matrix/out/19-autoscale-single-1-noazone-3gb.json

echo 'executing cost spec 20-autoscale-single-1-noazone-300gb.txt ...'
dotnet run spec_matrix/20-autoscale-single-1-noazone-300gb.txt > spec_matrix/out/20-autoscale-single-1-noazone-300gb.json

echo 'executing cost spec 21-autoscale-single-1-noazone-30000gb.txt ...'
dotnet run spec_matrix/21-autoscale-single-1-noazone-30000gb.txt > spec_matrix/out/21-autoscale-single-1-noazone-30000gb.json

echo 'executing cost spec 22-autoscale-multi-region-3-noazone-3gb.txt ...'
dotnet run spec_matrix/22-autoscale-multi-region-3-noazone-3gb.txt > spec_matrix/out/22-autoscale-multi-region-3-noazone-3gb.json

echo 'executing cost spec 23-autoscale-multi-region-3-noazone-300gb.txt ...'
dotnet run spec_matrix/23-autoscale-multi-region-3-noazone-300gb.txt > spec_matrix/out/23-autoscale-multi-region-3-noazone-300gb.json

echo 'executing cost spec 24-autoscale-multi-region-3-noazone-30000gb.txt ...'
dotnet run spec_matrix/24-autoscale-multi-region-3-noazone-30000gb.txt > spec_matrix/out/24-autoscale-multi-region-3-noazone-30000gb.json

echo 'executing cost spec 25-autoscale-multi-master-3-azone-3gb.txt ...'
dotnet run spec_matrix/25-autoscale-multi-master-3-azone-3gb.txt > spec_matrix/out/25-autoscale-multi-master-3-azone-3gb.json

echo 'executing cost spec 26-autoscale-multi-master-3-azone-300gb.txt ...'
dotnet run spec_matrix/26-autoscale-multi-master-3-azone-300gb.txt > spec_matrix/out/26-autoscale-multi-master-3-azone-300gb.json

echo 'executing cost spec 27-autoscale-multi-master-3-azone-30000gb.txt ...'
dotnet run spec_matrix/27-autoscale-multi-master-3-azone-30000gb.txt > spec_matrix/out/27-autoscale-multi-master-3-azone-30000gb.json

echo 'executing cost spec 28-autoscale-multi-master-3-noazone-3gb.txt ...'
dotnet run spec_matrix/28-autoscale-multi-master-3-noazone-3gb.txt > spec_matrix/out/28-autoscale-multi-master-3-noazone-3gb.json

echo 'executing cost spec 29-autoscale-multi-master-3-noazone-300gb.txt ...'
dotnet run spec_matrix/29-autoscale-multi-master-3-noazone-300gb.txt > spec_matrix/out/29-autoscale-multi-master-3-noazone-300gb.json

echo 'executing cost spec 30-autoscale-multi-master-3-noazone-30000gb.txt ...'
dotnet run spec_matrix/30-autoscale-multi-master-3-noazone-30000gb.txt > spec_matrix/out/30-autoscale-multi-master-3-noazone-30000gb.json
