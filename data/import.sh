#!/bin/bash

sqlite3 stockinfo.db << EOF
.separator ','
.import stock_tob.csv t_stock_tob
.quit
EOF