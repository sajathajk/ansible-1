#!/bin/sh

for page in Anforanden Ledamoter Voteringar Dokument
do
    cd ${OUTPUT1_STAGING_DIR}
    mkdir $page && cd $page
    curl -sS "http://data.riksdagen.se/Data/$page/" \
        | grep -io 'http://data\.riksdagen\.se.*\.json\.zip' \
        | sed 's/ /%20/' \
        | while read url; do echo "$url" && curl -fsSO "$url" ; done
#    for file in *.json.zip
#    do
#        unzip -d $(basename $file .json.zip) $file && rm $file
#    done
done
