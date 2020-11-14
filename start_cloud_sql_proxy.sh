#!/bin/bash -eo pipefail
cd "${BASH_SOURCE%/*}/" || exit
./cloud_sql_proxy -dir run/ -instances tdsmith-jira-helper:us-west1:jira-helper-mysql
