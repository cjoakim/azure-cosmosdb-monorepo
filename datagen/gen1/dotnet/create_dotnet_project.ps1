
# Use the dotnet CLI to bootstrap a dotnet project.
# Chris Joakim, Microsoft

echo ''
echo '=========='
echo 'checking dotnet --version  (6.0.x is expected)'
dotnet --version

echo ''
echo '=========='
echo 'creating project...'
dotnet new console -o CosmosLoader
cd     CosmosLoader

echo 'adding packages...'

dotnet add package Microsoft.Azure.Cosmos

# other packages of interest:
# dotnet add package CsvHelper
# dotnet add package DocumentFormat.OpenXml 
# dotnet add package Faker.Net
# dotnet add package Azure.Storage.Blobs
# dotnet add package Microsoft.EntityFrameworkCore.Cosmos
# dotnet add package Microsoft.EntityFrameworkCore.Sqlite
# dotnet add package Microsoft.Azure.DataLake.Store

cat    CosmosLoader.csproj
dotnet restore
dotnet list package
dotnet build
dotnet run

echo ''
echo 'done'
