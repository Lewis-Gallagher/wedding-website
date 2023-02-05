#!/bin/bash

mkdir -p ${PWD}/bak;
FILE=$1

if [ -f "$FILE" ]; then
    t=$(date "+%Y%m%d-%H%M%S");

    echo "Backing up ${FILE} to bak/${t}.${FILE}.sq3";

    sqlite3 ${FILE} ".backup 'bak/${t}.${FILE}.sq3'";

else
    echo "$FILE does not exist."
fi