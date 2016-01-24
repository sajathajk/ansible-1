#!/bin/sh

export PGPASSWORD=riksdagen
export PGUSER=riksdagen
export PGHOST=$1
export PGDATABASE=riksdagens_data

sudo yum install -y postgresql94

for i in ${INPUT1_STAGING_DIR}/*.sql.zip; do echo "$i" && unzip -p "$i"; done \
    | sed 's/\xEF\xBB\xBF//' \
    | sed 's/\[from\]/"from"/' \
    | sed 's/,,/,NULL,/g' \
    | sed 's/,,/,NULL,/g' \
    | psql
