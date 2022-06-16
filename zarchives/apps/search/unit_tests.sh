#!/bin/bash

# Execute the unit tests in this project with the pytest library.
# Chris Joakim, Microsoft, November 2021

source venv/bin/activate

python -m pytest tests/ 
