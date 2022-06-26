# azure-cosmosdb-monorepo - datagen/gen2

## Purpose

Create simulated **mongoexport** files for loading into MongoDB for migration testing.

---

## Public Datasets used in this Repo

- https://www.seanlahman.com/baseball-archive/statistics/
  - Download the [2021 – comma-delimited version [Baseball Databank] zip file](https://github.com/chadwickbureau/baseballdatabank/archive/refs/tags/v2022.2.zip)

This public data is augmented with some random values using the Python [Faker](https://pypi.org/project/Faker/).

### Attribution

The generated documents will each contain a "source_data_attribution" attribute, populated as follows: 

```
"source_data_attribution": "https://www.seanlahman.com/baseball-archive/statistics/",
```

---

## User Instructions

### System Requirements

- Windows 11, Linux, or macOS operating system
- Python 3
- Disk space sufficient for creating large datasets; 1GB or more is recommended.

### Clone this GitHub Repository

```
> git clone https://github.com/cjoakim/azure-cosmosdb-monorepo
> cd datagen
> cd gen2
```

### Download the Public Datasets

Download the above **2021 – comma-delimited version [Baseball Databank] zip file**
to directory **sourcedata/seanlahman/** in this repo.  Then unzip the file.

See file **seanlahman-baseballdatabank-files-list.txt** in this repo; after exploding
the downloaded zip file these files should exist on your system.

Confirm that file **sourcedata/seanlahman/baseballdatabank-2022.2/core/Batting.csv**
is present relative to the GitHub repo root directory on your computer.  This will
ensure that the csv files are in the correct location for the code in this repo.
You may have to copy the files up one directory.

### Setup and Activate the Python Virtual Environment

A Python Virtual Environment (i.e. - venv) specifies a version of Python and a set of
libraries to use within that environment.  You can have multiple virtual environments
on your computer.

The list of libraries is typically specified in a **requirements.in** or **requirements.txt**
file.

In this repo there are two scripts that can be executed to setup the Virtual Environment
for this project.  These are **venv.ps1** (Windows PowerShell) and **venv.sh** (bash, for Linux & macOS).
Execute the appropriate script.

See the comments at the end of these scripts which show how to **activate** the Virtual Environment
so that it will be used.

#### Activate Virtual Environment On Windows

```
> .\venv\Scripts\activate
```

#### Activate Virtual Environment On Linux and macOS

```
$ source venv/bin/activate
```

### Edit and Execute the Generate Scripts

These are **generate-baseball-data.ps1** (Windows PowerShell) and **generate-baseball-data.sh** (Bash, Linux & macOS).

The generated files are in **mongoexport/mongoimport** file format, and are located in the
**data/** directory of this repo.  These files are git-ignored.

#### On Windows

```
> .\generate-baseball-data.ps1
```

#### On Linux and macOS

```
$ ./generate-baseball-data.sh
```

### Sample Script

Both of the above scripts have lines like the following.  The values 50000 and 1000 refer to the
number of smaller and jumbo documents that will be generated, respectively.  Edit these counts
per the needs of your dataset.  At least one 2MB+ jumbo document will be generated.

```
python main.py create_baseball_base_mongoexport_files

python main.py create_baseball_large_document_count_data 50000

python main.py create_baseball_large_document_size_data 1000
```

### List of the Generated Files

The above **generate-baseball-data** scripts produce this list of 30 files:

```
baseball_contrib_AwardsManagers.json
baseball_contrib_AwardsPlayers.json
baseball_contrib_AwardsShareManagers.json
baseball_contrib_AwardsSharePlayers.json
baseball_contrib_CollegePlaying.json
baseball_contrib_HallOfFame.json
baseball_contrib_Salaries.json
baseball_contrib_Schools.json
baseball_core_AllstarFull.json
baseball_core_Appearances.json
baseball_core_Batting.json
baseball_core_BattingPost.json
baseball_core_Fielding.json
baseball_core_FieldingOF.json
baseball_core_FieldingOFsplit.json
baseball_core_FieldingPost.json
baseball_core_HomeGames.json
baseball_core_Managers.json
baseball_core_ManagersHalf.json
baseball_core_Parks.json
baseball_core_People.json
baseball_core_Pitching.json
baseball_core_PitchingPost.json
baseball_core_SeriesPost.json
baseball_core_Teams.json
baseball_core_TeamsFranchises.json
baseball_core_TeamsHalf.json
baseball_upstream_Teams.json

baseball_fantasy_teams_jumbo.json
baseball_fantasy_teams_small.json
```

The first 28 files have the same number of rows as their corresponding Seah Lahman Baseball Databank
CSV files.

The last two files (the baseball_fantasy_teams files), however, will be generated
with the number of rows you specify in the generate scripts.  This allows you
to create data as large as you need for migration testing.

### Generate the mongoimport scripts

This will generate PowerShell or Bash scripts which execute the **mongoimport**
program to load the JSON files generated above to your target MongoDB database.

#### On Windows

```
> .\generate-mongoimport-scripts.ps1
```

#### On Linux and macOS

```
$ ./generate-mongoimport-scripts.sh
```

**IMPORTANT NOTE:**

You may have to modify the **generate-mongoimport-scripts** and/or the
**templates/mongoimport.txt** so that the mongoimport program can connect
to your database.

---

## How to Run MongoDB locally as a Docker Container in WSL

See https://github.com/cjoakim/mongodb-docker.

```
$ git clone https://github.com/cjoakim/mongodb-docker
$ cd reference_app
$ cd mongo_docker
$ ./compose.sh up      <-- starts the Docker container with docker-compose

# Later, in another WSL Terminal in this same directory
$ ./compose.sh down    <-- stops the Docker container
```

---

## Sample Data 

There are 28 files in the seanlahman Baseball Databank.  This project creates
each as a mongoexport/mongoimport file.

Additionally, two files are created to create both **many documents** (i.e. - over 1-million)
as well as **jumbo documents** (i.e - up to 2MB and beyond).  These two files focus on Player
data that looks like the following for Roberto Clemente.

The **notes** array is random text created by the Faker library.


```
$ cat data/baseball_core_People.json | head -3347 | tail -1 | jq

{
  "_id": {
    "$oid": "6280fbc7b1cb828ff3d743c8"
  },
  "idx": 3347,
  "playerID": "clemero01",
  "birthYear": "1934",
  "birthMonth": "8",
  "birthDay": "18",
  "birthCountry": "P.R.",
  "birthState": "",
  "birthCity": "Carolina",
  "deathYear": "1972",
  "deathMonth": "12",
  "deathDay": "31",
  "deathCountry": "P.R.",
  "deathState": "",
  "deathCity": "San Juan",
  "nameFirst": "Roberto",
  "nameLast": "Clemente",
  "nameGiven": "Roberto",
  "weight": "175",
  "height": "71",
  "bats": "R",
  "throws": "R",
  "debut": "1955-04-17",
  "finalGame": "1972-10-03",
  "retroID": "clemr101",
  "bbrefID": "clemero01",
  "doctype": "core_People",
  "notes": [
    "General source energy speech carry hotel. Key security modern. The event professional anything charge kid hand.",
    "Theory fund full case fund see. Young simply article significant half recognize pressure.",
    "Official whether best color himself.",
    "Especially store letter great house.",
    "Style authority hit know purpose. Successful however many your positive issue."
  ],
  "source_data_attribution": "https://www.seanlahman.com/baseball-archive/statistics/",
  "_asz": 1057,
  "_generated_at": "2022-05-15T13:10:31.710461+00:00"
}
```

The **_asz** attribute represents approximate size of the document in bytes.

---

## Developer Notes

The remainder of this README is for notes related to the development of this project.
See the above for **User Instructions**.

### Python Libraries Used 

#### requirements.in

```
Faker
Jinja2
arrow
azure-storage-blob
docopt
flake8
humanize
pymongo
redis
requests
```

#### resulting list of libraries

```
$ pip list
Package            Version
------------------ ---------
arrow              0.17.0
azure-core         1.11.0
azure-storage-blob 12.7.1
certifi            2020.12.5
cffi               1.14.5
chardet            4.0.0
click              8.1.3
cryptography       3.4.6
docopt             0.6.2
Faker              13.11.1
flake8             3.8.4
humanize           3.2.0
idna               2.10
isodate            0.6.0
Jinja2             2.11.3
MarkupSafe         1.1.1
mccabe             0.6.1
msrest             0.6.21
oauthlib           3.1.0
pep517             0.12.0
pip                22.1
pip-tools          6.6.1
pycodestyle        2.6.0
pycparser          2.20
pyflakes           2.2.0
pymongo            3.11.3
python-dateutil    2.8.1
redis              3.5.3
requests           2.25.1
requests-oauthlib  1.3.0
setuptools         60.10.0
six                1.15.0
tomli              2.0.1
urllib3            1.26.3
wheel              0.37.1
```
