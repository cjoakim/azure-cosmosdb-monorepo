# azure-cosmosdb-monorepo - datagen/gen1

Data generators for use in Azure, such as documents for CosmosDB

Implemented in python3 and DotNet 6.

---

## python3

python is used in this repo to **generate** the sample data.

Instructions below are for PowerShell, but equivalent bash scripts
for linux/mac are also in this repo.

```
cd python
.\venv.ps1                    <-- creates python virtual environment (venv)
.\venv\Scripts\Activate.ps1   <-- activate the virtual environment

python main.py gen_customers 1000
python main.py gen_products 1000
python main.py gen_aus_online_txn 2021-02-25 2022-02-25 100 > data\online_txn.json
python main.py gen_aus_flybuy_txn 2021-02-25 2022-02-25 100 > data\flybuy_txn.json
```

See **gen_aus_data.ps1**, as executed below:

```
(venv) PS ...\python> .\gen_aus_data.ps1
generating customers ...
gen_customers, 1000
file_written: data/customers.json
generating products ...
gen_products, 1000
file_written: data/products.json
generating online txns using customers and products, redirecting to file ...
generating flybuy txns using customers and products, redirecting to file ...
done
```

#### Linux / macOS / WSL

```
$ ./venv.sh
...

$ source venv/bin/activate

(venv) [~/github/azure-datagen/python]$ python main.py gen_customers 1000
file_written: data/customers.json
```

---

## DotNet 6

DotNet is used in this repo to **load** the generated sample data
into CosmosDB/Core.

### Environment Variables

The following are assumed to be present and populated; see your CosmosDB/Core
account in Azure Portal:

```
AZURE_COSMOSDB_SQLDB_CONN_STRING
AZURE_COSMOSDB_SQLDB_KEY
AZURE_COSMOSDB_SQLDB_URI
AZURE_COSMOSDB_SQLDB_PREF_REGIONS
AZURE_COSMOSDB_BULK_BATCH_SIZE  
```

In Windows PowerShell, you can set environment variables as follows:

```
[Environment]::SetEnvironmentVariable("AZURE_COSMOSDB_SQLDB_URI", "<your-value>", "User")
```

### Compile, Build, Execute

```
dotnet restore
dotnet build
dotnet run list_databases
dotnet run list_containers dev
dotnet run list_containers <dbname>

dotnet run bulk_load_container <dbname> <container> <pk-attr> <infile> <batch-size>
dotnet run bulk_load_container dev online_txn pk data\online_txn.json 500

dotnet run count_documents <dbname> <cname>
dotnet run count_documents dev online_txn
```

See Program.cs for other functionality not listed here.
