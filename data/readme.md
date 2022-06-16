# azure-cosmosdb-monorepo - data directory

This directory contains subdirectories with sample datasets for various
domains - travel, airports, postal codes, graph, etc.

## python data-wrangling code

Also in this directory is the following minimal set of **python** files
for **"data-wrangling**" and creating these datasets.

```
pysrc/            <-- custom code libraries
requirements.in   <-- the raw minimal list of PyPi libraries
requirements.txt  <-- the pip-compiled list of PyPi libraries
templates/        <-- Jinja2 text templates>
venv.ps1          <-- creates a python virtual environment, on Windows, from libs in requirements.in
venv.sh           <-- creates a python virtual environment, on Linux/WSL/macOS, from libs in requirements.in
wrangle.py        <-- "main" program for data wrangling
xamples.py        <-- example "main" program; uses the custom code libs in pysrc/
```
