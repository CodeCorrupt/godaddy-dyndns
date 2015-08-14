#!/bin/bash

set -e

ROOT_DIR=$(dirname $0)
cd $ROOT_DIR

if [[ ! -d venv ]]; then
    echo "venv not initialized!" >& 2
    exit 1
fi

source venv/bin/activate
./godaddy-dyndns.py
