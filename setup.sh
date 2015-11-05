#!/bin/bash

git submodule init
git submodule update

cp godaddy-dyndns.conf.template godaddy-dyndns.conf

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
deactivate
