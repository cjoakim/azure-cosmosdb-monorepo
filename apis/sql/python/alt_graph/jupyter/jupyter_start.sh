#!/bin/bash

# List the available kernels, then start jupyter.
# Chris Joakim, Microsoft, June 2022

# This command only needs to be executed once, then select this kernel in
# the Jupyter UI with "Kernel -> Change Kernel" after opening a notebook. 
ipython kernel install --name "alt_graph" --user

echo 'listing available kernels ...'
jupyter kernelspec list

echo 'starting jupyter notebook ...'
jupyter notebook
