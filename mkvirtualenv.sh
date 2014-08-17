#!/usr/bin/env bash

#
# Creates python environment for building site, assuming virtualenv is already available
# No need to create this environment when using Travis for deployment
#

# Create virtualenv in ./env
virtualenv env

# Activate virtual environment
source env/bin/activate

# Install dependencies via pip
pip install -r requirements.txt 
