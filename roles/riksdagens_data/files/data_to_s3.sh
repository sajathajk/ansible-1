#!/bin/sh

cd "${OUTPUT1_STAGING_DIR}"

curl -sS "http://data.riksdagen.se/Data/{Anforanden,Ledamoter,Voteringar,Dokument}/" \
    | grep -io 'http://data\.riksdagen\.se.*\.sql\.zip' \
    | sed 's/ /%20/' \
    | while read i; do echo "$i" && curl -O "$i" ; done
