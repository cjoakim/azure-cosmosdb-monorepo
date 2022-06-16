# azure-cognitive-search-example

<p align="center" width="95%">
  <img src="img/azure-cognitive-search-example.png">
</p>

---

## Project Overview 

This github project demonstrates an Azure Solution based on **Azure Cognitive Search**,
and other Azure PaaS services, including:
- **Azure Cognitive Service** - used by the Search service to invoke **built-in** skills
- **Azure Storage** - stores documents to be indexed
- **Azure CosmosDB** w/SQL API  - stores documents to be indexed
- **Azure Function** implemeting a HTTP-triggered **Custom Cognitive Skill**

Two **Indexes** are created in this project:
- **Airports** - US Airports in JSON format in **CosmosDB**
  - Simple text-based indexing, minimal dependent PaaS services
- **Documents** - PDF, image, and HTML files in **Storage**
  - Advanced document-cracking, knowledge mining, and AI 

**Python 3** is used as the sole programming language for this project, to do the following:
- Generate **JSON schemas** which are used extensively by Azure Cognitive Search 
- Upload a curated set of documents to Azure Storage; see the documents/ directory
- Upsert JSON Airport documents to CosmosDB; see file data/us_airports.json
- Implement the Custom Cognitive Skill Azure Function; see the FunctionApp/ directory
- Invoke the **REST API** of the **Azure Cognitive Search**, using the **requests** library to POST the generated schemas

Python 3 was chosen because it is cross-platform, practical, and is commonly used by Data Scientists.

The initial implementation of this project focuses on the **bash** shell and the **linux** 
and **macOS** operating systems, but **Windows** and **PowerShell** support will be added
in the near future.  In the meanwhile, the bash shell scripts in this repo **do** work with 
the Windows Subsystem for Linux (WSL); see https://docs.microsoft.com/en-us/windows/wsl/install-win10

---

## Provisioning Azure Resources

In Azure you can provision resources in one of several ways, including the **Azure Portal**, **ARM templates**, the **az CLI**, and others.

Several scripts using the **az CLI** are provided in this repo; I recommend using the Azure Portal Web UI to create the others.

The az CLI scripts are located in directory **automation/az/**.

Edit file **config.sh** in this directory per your desired Azure Region, Resource Group, and resource names.

### Azure Cognitive Search

```
$ ./search.sh create
```

### Azure Cognitive Service

```
$ ./cognitive.sh create
```

Note: In order for this az provisioning script to work, your Azure account 
must have a Cognitive Services Contributor role assigned.  The alternative
solution is to simply provision the CognitiveServices account in Azure Portal.

### Azure Storage

In Azure Portal, create a Storage account of type **StorageV2 (general purpose v2)**.

In this project, a SDK client will upload documents to be indexed to Azure Storage.
Alternatively, [Azure Storage Explorer](https://azure.microsoft.com/en-us/features/storage-explorer/) can be used to upload the documents.

Or, provision with the az CLI:

```
$ ./storage.sh create
```

### Azure CosmosDB

In Azure Portal create a **Cosmos/SQL** account.  

After you create the Account, go to the **Features** panel and enable the
**Azure Synapse Link** feature.

Then add a **dev** database, with an **airports** container specifying a partition key field named **/pk**.  400 RUs (Request Units) is adequate for this project.

When you create the container, also enable the **Analytical Store** for using **Synapse Link**.

### Azure Function

Create a Function app with your tool-of-choice; Visual Studio, Visual Studio Code, or the
**func** command line tools.  See https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local?tabs=macos%2Ccsharp%2Cbash

I used the **func** command line tools; see the section below titled 
**Custom Skill Azure Function**.

---

## Environment Variables

Using environment variables is a "best practice" for handling configuration values on your
workstation.  Using these enables you to eliminate "hard coded" configuration values and
secrets.

This project uses the following environment variables; some example values are shown.
These values can be obtained from Azure Portal once your above resources have been created;
see the keys section of the UI for each service.

Please use your own name, and not cjoakim, for your Azure Services!

```
AZURE_SUBSCRIPTION_ID= ... your Azure Subscription Id ...
AZURE_COSMOSDB_SQLDB_ACCT=cjoakimcosmossql
AZURE_COSMOSDB_SQLDB_KEY= ... secret ...
AZURE_COSMOSDB_SQLDB_URI=https://cjoakimcosmossql.documents.azure.com:443/
AZURE_SEARCH_STORAGE_ACCOUNT=cjoakimsearch
AZURE_SEARCH_STORAGE_KEY= ... secret ...
AZURE_SEARCH_STORAGE_CONNECTION_STRING= ... secret ...
AZURE_SEARCH_NAME=cjoakimsearch
AZURE_SEARCH_URL=https://cjoakimsearch.search.windows.net
AZURE_SEARCH_ADMIN_KEY= ... secret ...
AZURE_SEARCH_QUERY_KEY= ... secret ...
AZURE_SEARCH_COGSVCS_ALLIN1_KEY= ... secret ...
AZURE_FUNCTION_CUSTOM_SKILL_LOCAL=http://localhost:7071/api/TopWordsSkill
AZURE_FUNCTION_CUSTOM_SKILL_REMOTE=https://cjoakimsearchapp.azurewebsites.net/api/TopWordsSkill?code=...secret...
```

---

## Concepts

- [HTTP REST API](https://docs.microsoft.com/en-us/rest/api/searchservice/)
  - [HTTP Status Codes](https://docs.microsoft.com/en-us/rest/api/searchservice/http-status-codes)
  - [HTTP Status Codes; Explained as Dogs](https://httpstatusdogs.com)
  - [Python Requests Library; HTTP for Humans](https://requests.readthedocs.io/en/master/)
- [Indexes](https://docs.microsoft.com/en-us/azure/search/search-what-is-an-index)
  - A search index stores searchable content, called Documents, used for full text and filtered queries
- [Index from Storage](https://docs.microsoft.com/en-us/azure/search/search-blob-storage-integration)
- [Index from CosmosDB, and document "flattening"](https://docs.microsoft.com/en-us/azure/search/search-howto-index-cosmosdb)
- [Indexers](https://docs.microsoft.com/en-us/azure/search/search-indexer-overview)
  - An indexer in is a crawler that extracts searchable data and metadata from an external Azure data source and populates an index based on field-to-field mappings.
  - An indexer **cracks** binary documents (PDF, Word, Images, etc) to extract their text
- [Synonyms](https://docs.microsoft.com/en-us/azure/search/search-synonyms)
  - Synonyms in search engines associate equivalent terms
- [Skillsets](https://docs.microsoft.com/en-us/azure/search/cognitive-search-defining-skillset)
  - A skillset is an optional collection of cognitive skills used for AI enrichment of the indexed documents
- [Skills and Document Cracking](https://docs.microsoft.com/en-us/azure/search/cognitive-search-concept-intro)
- [Built-In Skills](https://docs.microsoft.com/en-us/azure/search/cognitive-search-predefined-skills)
- [Custom Skills](https://docs.microsoft.com/en-us/azure/search/cognitive-search-defining-skillset#add-a-custom-skill)

---

### JSON Schemas

**JSON schemas** are used extensively by Azure Cognitive Search to configure
the various objects - Datasources, Indexes, Indexers, Skillsets, Synonyms.

#### Documentation Links

- [Index](https://docs.microsoft.com/en-us/rest/api/searchservice/create-index)
- [Datasource](https://docs.microsoft.com/en-us/rest/api/searchservice/create-data-source)

#### Schemas used in this Project

- [Datasource CosmosDB](schemas/datasource-cosmosdb-dev-airports.json)
- [Datasource Storage](schemas/datasource-azureblob-documents.json)
- [Airports Index](schemas/airports_index_v1.json)
- [Airports Indexer](schemas/airports_indexer_v1.json)
- [Documents Index](schemas/documents_index_v1.json)
- [Documents Indexer](schemas/documents_indexer_v1.json)
- [Documents Skillset](schemas/skillset_v1.json)
- [Synonyms](schemas/synonym_map_v1.json)

### Other Links

- [Azure Cognitive Search Overview](https://azure.microsoft.com/en-us/services/search/)
- [Azure Cognitive Search Documentation](https://docs.microsoft.com/en-us/azure/search/)
- [REST API](https://docs.microsoft.com/en-us/rest/api/searchservice/)
- [AI Enrichment](https://docs.microsoft.com/en-us/azure/search/cognitive-search-concept-intro)
- [Data Types](https://docs.microsoft.com/en-us/rest/api/searchservice/supported-data-types)
- [API Versions](https://docs.microsoft.com/en-us/rest/api/searchservice/search-service-api-versions)
- [Postman HTTP Client UI](https://www.postman.com)
- [curl HTTP Client CLI program](https://curl.haxx.se/docs/httpscripting.html)

---

## Implementation and Execution

**This project is implemented using shell scripts, python programming, and JSON files.**

First, you'll need to clone this repository and create the python virtual environment
as shown here.

```
$ git clone https://github.com/cjoakim/azure-cognitive-search-example.git
$ cd azure-cognitive-search-example

$ mkdir tmp                      <-- some output files are written to the tmp/ directory

$ ./venv.sh create               <-- create the python virtual environment, with "venv" standard library
$ source venv/bin/activate       <-- activate the python virtual environment

$ ./pyenv.sh create              <-- alternative way to create python virtual environment, with "pyenv" program
```

### Airports Index

To create the **airports** Index run the following script.  The airports index does **not** 
require the Azure Cognitive Service, Azure Storage, Azure Function, but it does require Azure CosmosDB.

```
$ ./recreate_airports.sh
```

#### Sample CosmosDB Document

```
    {
        "name": "Charlotte Douglas Intl",
        "city": "Charlotte",
        "country": "United States",
        "iata_code": "CLT",
        "latitude": "35.214",
        "longitude": "-80.943139",
        "altitude": "748",
        "timezone_num": "-5",
        "timezone_code": "America/New_York",
        "location": {
            "type": "Point",
            "coordinates": [
                -80.943139,
                35.214
            ]
        },
        "id": "f0ad3291-d2e5-4199-8d78-a96578755656",
        "pk": "CLT",
        "epoch": 1637336812.363724,
        "_rid": "f0p9AJj1bKDvAQAAAAAAAA==",
        "_self": "dbs/f0p9AA==/colls/f0p9AJj1bKA=/docs/f0p9AJj1bKDvAQAAAAAAAA==/",
        "_etag": "\"0e00f65f-0000-0100-0000-6197c6ec0000\"",
        "_attachments": "attachments/",
        "_ts": 1637336812
    }
```

### Documents Index

To create the **documents** Index, from Azure Storages blobs (PDFs, Images, html files) run the following script.
You'll also need to first create your Azure Function, as described below in section "Custom Skill Azure Function".
This index does **not** use CosmosDB, but it does use the other Azure PaaS services listed above.

```
$ ./recreate_documents.sh
```

**See each of these scripts for the details.  But essentially they create a datasource, an index, and and indexer
for each index after uploading the underlying documents to Azure Storage or Azure CosmosDB.  All of these
actions are done in code with Python, and interact with the Azure Search Service via the REST API.**

### The Python Code

- [base.py](base.py) - Implements the abstract BaseClass inherited by the other classes below
- [search-client.py](search-client.py) - Implements class SearchClient and **invokes the Azure Cognitive Search REST API**
- [storage-client.py](storage-client.py) - Implements class StorageClient and uploads the documents to Azure Storage
- [cosmos.py](cosmos.py) - Implements class CosmosClient and uploads US Airport documents to CosmosDB
- [schemas.py](schemas.py) - Used by class SearchClient to generate and load JSON Schemas from files
- [urls.py](urls.py) - Used by class SearchClient to create the many REST API URLs from dynamic parameters
- The tests/ directory - contains unit tests which use the **pytest** library; see unit_tests.sh

---

## Skillset

An optional **Skillset**, containing **Skills**, can be used in a **pipeline** by the Indexer to
augment the raw text extracted from the documents.  Skills can be either **built-in** or **custom**.

The Skillset in this project uses the following Skills in the pipeline;
see file schemas/skillset_v1.json.  This Skillset pipeline greatly augments
the raw extracted text, and transforms a simple **Search App** into an AI-driven 
**Cognitive Search App**.

For example, PDF and other documents are **cracked** and their embedded text and 
images are further analyzed for **Entity Recognition, Sentiment, Key Phrases, and Image Analysis**.

The implementations of **WebApiSkills** are up to you and are only limited by your creativity.  In this app, the WebApiSkill invokes the Azure Function to identify the
top n-number of words in the combined mergedText of the document (i.e. - document 
and image text). 

```
$ cat schemas/skillset_v1.json | grep odata

      "@odata.type": "#Microsoft.Skills.Text.EntityRecognitionSkill",
      "@odata.type": "#Microsoft.Skills.Text.SentimentSkill",
      "@odata.type": "#Microsoft.Skills.Text.KeyPhraseExtractionSkill",
      "@odata.type": "#Microsoft.Skills.Vision.OcrSkill",
      "@odata.type": "#Microsoft.Skills.Text.MergeSkill",
      "@odata.type": "#Microsoft.Skills.Vision.ImageAnalysisSkill",
      "@odata.type": "#Microsoft.Skills.Custom.WebApiSkill",
      "@odata.type": "#Microsoft.Azure.Search.CognitiveServicesByKey",
```

### OCR, Image Analysis, and TopWords - Sample Outputs

The [OCR](https://docs.microsoft.com/en-us/azure/search/cognitive-search-skill-ocr) and 
[Image Analysis](https://docs.microsoft.com/en-us/azure/search/cognitive-search-skill-image-analysis)
built-in Skills are used to **crack** the indexed documents to extract their embedded text, 
as well as leveraging AI to recognize the contents of the image.  The **TopWords Custom WebApiSkill**
is implemented as an Azure Function


#### Of the above diagram

```
"imageDescription": [
  "{\"tags\":[\"diagram\"],\"captions\":[{\"text\":\"diagram\",\"confidence\":0.82125532627105713}]}"
],
"imageText": [
  "Azure Cognitive Search Example Concepts: - Paas - Datasource - Index - Indexer - Synonyms - Knowledge Mining - Built-in Skills Custom Skill - Custom Skills Function (HTTP) - Skillset - Search - Lookup O Cognitive Service ( Built-in Skills - OCR, etc. ) REST API HTTP Client Azure ( Console Program ) Cognitive Search Python Client CosmosDB Datasource ( loader program ) Azure Storage Explorer Blob Storage Datasource Python Client (PDFs, Images, Html, etc.) ( loader program ) Https://github.com/cjoakim/azure-cognitive-search-example"
],
"mergedText": " Azure Cognitive Search Example Concepts: - Paas - Datasource - Index - Indexer - Synonyms - Knowledge Mining - Built-in Skills Custom Skill - Custom Skills Function (HTTP) - Skillset - Search - Lookup O Cognitive Service ( Built-in Skills - OCR, etc. ) REST API HTTP Client Azure ( Console Program ) Cognitive Search Python Client CosmosDB Datasource ( loader program ) Azure Storage Explorer Blob Storage Datasource Python Client (PDFs, Images, Html, etc.) ( loader program ) Https://github.com/cjoakim/azure-cognitive-search-example \n",
"topwords": [
  "azure",
  "cognitive",
  "search",
  "datasource",
  "skills",
  "client",
  "program",
  "built-in",
  "custom",
  "http",
  "etc",
  "python",
  "loader",
  "storage",
  "example",
  "concepts:",
  "paas",
  "index",
  "indexer",
  "synonyms"
]
```

---

#### Of a UPS Truck

<p align="center" width="95%">
  <img src="documents/UPSWEB-800x533.jpg">
</p>

```
"imageDescription": [
  "{\"tags\":[\"outdoor\",\"truck\",\"road\",\"transport\",\"parked\",\"car\",\"front\",\"sitting\",\"side\",\"bus\",\"large\",\"street\",\"parking\",\"standing\",\"old\",\"green\",\"man\"],\"captions\":[{\"text\":\"a truck is parked on the side of a road\",\"confidence\":0.96122339571435267}]}"
],
"imageText": [
  "ups 150472 Worldwide Services Low Emission Hybrid Electric Vehicle USDOT 021800"
],
"mergedText": " ups 150472 Worldwide Services Low Emission Hybrid Electric Vehicle USDOT 021800 \n",
"topwords": [
  "ups",
  "150472",
  "worldwide",
  "services",
  "low",
  "emission",
  "hybrid",
  "electric",
  "vehicle",
  "usdot",
  "021800"
]
```

---

#### Of a Marathon Finish

<p align="center" width="95%">
  <img src="documents/sfny.jpg">
</p>

```
"imageDescription": [
  "{\"tags\":[\"person\",\"road\",\"outdoor\",\"sport\",\"street\",\"man\",\"walking\",\"holding\",\"woman\",\"people\",\"jumping\",\"young\",\"standing\",\"riding\",\"city\",\"playing\",\"player\",\"group\",\"ball\"],\"captions\":[{\"text\":\"Shalane Flanagan et al. walking down the street\",\"confidence\":0.7455881694062344}]}"
],
"imageText": [
  "B TATA CONSULTANCY SERVICES TATA TCS NEW FLANAGAN 2017 % WOR YORK CITY airbnb"
],
"mergedText": " B TATA CONSULTANCY SERVICES TATA TCS NEW FLANAGAN 2017 % WOR YORK CITY airbnb \n",
"topwords": [
  "tata",
  "consultancy",
  "services",
  "tcs",
  "new",
  "flanagan",
  "2017",
  "wor",
  "york",
  "city",
  "airbnb"
]
```

---

## Custom Skill Azure Function

Creating the Azure Function with the CLI tooling.

First, create the Function App, which will contain the Function(s):

```
az functionapp create \
  --resource-group AzureFunctionsQuickstart-rg \
  --os-type Linux \
  --consumption-plan-location eastus \
  --runtime python \
  --runtime-version 3.7 \
  --functions-version 2 \
  --name <APP_NAME> \
  --storage-account <STORAGE_NAME>
```

Then use the **func** utility to generate and deploy the Azure Function to the Function App.

```
$ func init --help
$ func init FunctionApp --worker-runtime python

$ cd FunctionApp

$ func new --name TopWordsSkill --template "HTTP trigger"

$ ./venv.sh    (with an empty requirements.in file)

  ... edit the generated TopWordsSkill/__init__.py file, which implements the Function ...

$ func start
Found Python version 3.8.5 (python3).
Azure Functions Core Tools (3.0.2912 Commit hash: bfcbbe48ed6fdacdf9b309261ecc8093df3b83f2)
Function Runtime Version: 3.0.14287.0
Hosting environment: Development
Now listening on: http://0.0.0.0:7071
Application started. Press Ctrl+C to shut down.

Functions:
	TopWordsSkill: [GET,POST] http://localhost:7071/api/TopWordsSkill
```

Invoke the HTTP Function, running locally, from another Terminal.

```
$ python search-client.py invoke_local_function pyf-onedrop.png
```

After you're satisfied with how the Function runs locally, deploy it to Azure:

```
$ func azure functionapp publish $app_name
  - or -
$ ./publish.sh
```

---

## Searching!

Finally, the purpose of an **Azure Cognitive Search** solution is to have the ability
to search the contents (i.e. - the Indices) in a fluent and accurate manner.

There are two query syntaxes available for your use - the **simple syntax** and the
**lucene syntax**.  Examples of each are shown below.  Either syntax is much more
complex and full-featured than SQL.  Simple syntax is the default.  Lucene syntax can be 
specified with the "queryType": "full" parameter.

### Links

- [Simple Query Syntax](https://docs.microsoft.com/en-us/azure/search/query-simple-syntax)
- [Lucene Query Syntax](https://docs.microsoft.com/en-us/azure/search/query-lucene-syntax)

### A Note about Command-Line Programs and Search Syntax

Since the format of the search parameters can get quite complex, it would be very awkward
to pass them on the command-line to the **search-client.py** program.  Instead, the approach
I took in this project was to implement **named queries**.  Just the name of the query is
passed in on the command-line, and the parameters for each named query are defined in file
**searches.json**; file shown below:

```
{
  "all_airports": {
    "count": true,
    "search": "*",
    "orderby": "pk"
  },
  "airports_charl": {
    "count": true,
    "search": "charl*",
    "orderby": "pk",
    "select": "name,city,pk"
  },
  "airports_lucene_east_cl": {
    "count": true,
    "search": "timezone_code:New_York~ AND pk:CL*",
    "orderby": "pk",
    "select": "pk,name,city,latitude,timezone_code",
    "queryType": "full"
  },
  "airports_lucene_east_cl_south": {
    "count": true,
    "search": "timezone_code:New_York~ AND pk:CL*",
    "filter": "latitude lt 39",
    "orderby": "pk",
    "select": "pk,name,city,latitude,timezone_code",
    "queryType": "full"
  },
  "all_documents": {
    "count": true,
    "search": "*",
    "orderby": "id"
  },
  "large_documents": {
    "count": true,
    "search": "*",
    "filter": "size gt 10000000",
    "select": "id,url,size,topwords",
    "orderby": "id"
  },
  "top_words_python": {
    "count": true,
    "search": "python,searchFields=topwords",
    "select": "id,url,size,topwords",
    "orderby": "id"
  },
  "top_words_flanagan": {
    "count": true,
    "search": "flanagan,searchFields=topwords",
    "select": "id,url,size,topwords",
    "orderby": "id"
  },
  "keyphrase_adventurous_little_sloop": {
    "count": true,
    "search": "adventurous little sloop,searchFields=keyPhrases",
    "select": "id,url,size,keyPhrases",
    "skip": 0,
    "top": 1,
    "orderby": "search.score() desc"
  },
  "nebraska": {
    "count": true,
    "search": "nebraska,searchFields=imageText",
    "select": "id,url,size,topwords",
    "orderby": "id"
  },
  "moscow": {
    "count": true,
    "search": "moscow,searchFields=imageText",
    "select": "id,url,size",
    "orderby": "id"
  },
  "moscow_with_text": {
    "count": true,
    "search": "moscow,searchFields=imageText",
    "select": "id,url,size,topwords,mergedText",
    "orderby": "id"
  },
  "pandas_as_in_bear": {
    "count": true,
    "search": "pandas bear giant,searchFields=imageText,mergedText",
    "select": "id,url,size",
    "skip": 0,
    "top": 2,
    "orderby": "search.score() desc"
  },
  "pandas_as_in_python": {
    "count": true,
    "search": "pandas dataframe,searchFields=imageText,mergedText",
    "select": "id,url,size",
    "skip": 0,
    "top": 2,
    "orderby": "search.score() desc"
  },
  "python_as_in_code": {
    "count": true,
    "search": "python programming code,searchFields=imageText,mergedText",
    "select": "id,url,size",
    "skip": 0,
    "top": 3,
    "orderby": "search.score() desc"
  },
  "python_as_in_snake": {
    "count": true,
    "search": "python snake,searchFields=imageText,mergedText",
    "select": "id,url,size",
    "skip": 0,
    "top": 1,
    "orderby": "search.score() desc"
  }
}
```

### Invoking the Searches

The command line format is:
```
$ python search-client.py search_index [index-name] [search-name]
```

#### Example 1 - Airports, East Coast USA, CL*, in the South

For example, let's search for Airports that are in the New York timezone, 
have an partition key (i.e. - iata code) that begins with CL*, and are South 
of the Mason-Dixon line.

```
$ python search-client.py search_index airports airports_lucene_east_cl_south
```

Notice how the parameters for this named search, as defined in the JSON file, are used
for the HTTP POST to the Azure Cognitive Search URL.  This produces the following output:

```
...
url:    https://cjoakimsearch.search.windows.net/indexes/airports/docs/search?api-version=2020-06-30
params: {'count': True, 'search': 'timezone_code:New_York~ AND pk:CL*', 'filter': 'latitude lt 39', 'orderby': 'pk', 'select': 'pk,name,city,latitude,timezone_code', 'queryType': 'full'}
response: <Response [200]>
{
  "@odata.context": "https://cjoakimsearch.search.windows.net/indexes('airports')/$metadata#docs(*)",
  "@odata.count": 2,
  "value": [
    {
      "@search.score": 1.8593993,
      "pk": "CLT",
      "name": "Charlotte Douglas Intl",
      "city": "Charlotte",
      "latitude": 35.214,
      "timezone_code": "America/New_York"
    },
    {
      "@search.score": 1.8823843,
      "pk": "CLW",
      "name": "Clearwater Air Park",
      "city": "Clearwater",
      "latitude": 27.9764722,
      "timezone_code": "America/New_York"
    }
  ]
}
response document count: 2
file written: tmp/airports_lucene_east_cl_south.json
```

#### Example 2 - Documents, Flanagan in Topwords

Let's search just the **topwords** field of the documents index for the word (name)
**flanagan**.

```
$ python search-client.py search_index documents top_words_flanagan
...
url:    https://cjoakimsearch.search.windows.net/indexes/documents/docs/search?api-version=2020-06-30
params: {'count': True, 'search': 'flanagan,searchFields=topwords', 'select': 'id,url,size,topwords', 'orderby': 'id'}
response: <Response [200]>
{
  "@odata.context": "https://cjoakimsearch.search.windows.net/indexes('documents')/$metadata#docs(*)",
  "@odata.count": 1,
  "value": [
    {
      "@search.score": 7.8584824,
      "id": "aHR0cHM6Ly9jam9ha2ltc2VhcmNoLmJsb2IuY29yZS53aW5kb3dzLm5ldC9kb2N1bWVudHMvc2ZueS5qcGc1",
      "url": "https://cjoakimsearch.blob.core.windows.net/documents/sfny.jpg",
      "size": 354574,
      "topwords": [
        "tata",
        "consultancy",
        "services",
        "tcs",
        "new",
        "flanagan",
        "2017",
        "wor",
        "york",
        "city",
        "airbnb"
      ]
    }
  ]
}
response document count: 1
file written: tmp/top_words_flanagan.json
```

The returned document represents the image (shown above) of Shalane Flanagan winning the 2017 New York City Marathon.
The actual image file can then be read from Azure Storage using the returned URL.

This search demonstrates that **Azure Cognitive Search** is more than a simple search engine;
it is an ***AI-driven Cognitive*** search engine.  In the case of this jpg image document, the 
text was first extracted from the built-in **OcrSkill**.  Then, the top extracted words were 
identified and added to the index by our custom **WebApiSkill** (Azure Function) and made searchable.

#### Example 3 - Documents, Moscow in imageText

Let's search just the **imageText** field of the documents index for the word (name)
**moscow**.  Hint; it's a [town in Idaho]('https://en.wikipedia.org/wiki/Moscow,_Idaho')

```
$ python search-client.py search_index documents moscow
- or -
$ python search-client.py search_index documents moscow_with_text

url:    https://cjoakimsearch.search.windows.net/indexes/documents/docs/search?api-version=2020-06-30
params: {'count': True, 'search': 'moscow,searchFields=imageText', 'select': 'id,url,size', 'orderby': 'id'}
response: <Response [200]>
{
  "@odata.context": "https://cjoakimsearch.search.windows.net/indexes('documents')/$metadata#docs(*)",
  "@odata.count": 1,
  "value": [
    {
      "@search.score": 5.1123643,
      "id": "aHR0cHM6Ly9jam9ha2ltc2VhcmNoLmJsb2IuY29yZS53aW5kb3dzLm5ldC9kb2N1bWVudHMvQW10cmFrLVN5c3RlbS1NYXAtMTAxOC5wZGY1",
      "url": "https://cjoakimsearch.blob.core.windows.net/documents/Amtrak-System-Map-1018.pdf",
      "size": 3059380
    }
  ]
}
response document count: 1
file written: tmp/moscow.json
```

#### Example 4 - Documents, Python - Code vs Snakes

```
$ python search-client.py search_index documents python_as_in_code
$ python search-client.py search_index documents python_as_in_snake
```

These two searches use the following parameters; see **searches.json**
```
  "python_as_in_code": {
    "count": true,
    "search": "python programming code,searchFields=imageText,mergedText",
    "select": "id,url,size",
    "skip": 0,
    "top": 3,
    "orderby": "search.score() desc"
  },
  "python_as_in_snake": {
    "count": true,
    "search": "python snake,searchFields=imageText,mergedText",
    "select": "id,url,size",
    "skip": 0,
    "top": 1,
    "orderby": "search.score() desc"
  }
```

#### Other Examples

```
$ python search-client.py search_index documents pandas_as_in_bear
$ python search-client.py search_index documents pandas_as_in_python
$ python search-client.py search_index documents keyphrase_adventurous_little_sloop
```
