#!/bin/bash

sqlite3 stockinfo.db << EOF
.separator ','
.output stock_tob_export.csv
select * from t_stock_tob;
.output stdout
.quit
EOF