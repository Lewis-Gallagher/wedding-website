#!/bin/bash

mkdir -p ${PWD}/bak;
FILE=${PWD}/app.db

if [ -f "$FILE" ]; then
    t=$(date "+%Y%m%d-%H%M%S");

    echo "Backing up app.db to bak/${t}.app.db.sq3";

    sqlite3 app.db ".backup 'bak/${t}.app.db.sq3'";

else
    echo "$FILE does not exist."
fi
