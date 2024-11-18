#!/bin/bash

DIR_NAME="shp_cat"

mkdir -p $DIR_NAME 
cd $DIR_NAME


wget https://datacloud.icgc.cat/datacloud/divisions-administratives/shp/divisions-administratives-v2r1-20240705.zip

unzip *.zip

# keep only shp data

#ls | grep -v shp | xargs rm

# keep only highres

ls | grep -v "1000000" | xargs rm