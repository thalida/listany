#!/bin/bash
set -o allexport
source /workspaces/listany/.env
# source /workspaces/listany/app/.env
set +o allexport

cd /workspaces/listany/api
poetry install

# cd /workspaces/listany/app
# npm install
