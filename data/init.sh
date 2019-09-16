#!/bin/bash

sqlite3 stockinfo.db << EOF
. read create.sql
.quit
EOF