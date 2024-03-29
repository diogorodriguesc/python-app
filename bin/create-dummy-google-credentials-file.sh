#!/usr/bin/env bash

file=/tmp/dummy_google_credentials_file.json

rm $file
touch $file
echo '{"projectid": "sitemaps_dev"}' > $file # sure this is dummy and temporary and I am not going to put any out here

echo "To create the env var run the following:"

echo "export SITEMAPS_INDEXING_GOOGLE_CREDENTIALS=$file"
echo "export SITEMAPS_INDEXING_DB_PASSWORD=root"
