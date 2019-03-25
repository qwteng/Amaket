__author__ = 'qwteng'

import logging
from amarket.ds.data_source import *
from amarket.data_preprocess import *
from amarket.utils.timeUtils import *


ts_api = get_tsapi()
end_date = datetime.now().strftime("%Y%m%d")
offset = -7
start_date = get_workday(end_date, -7)
file_reslult = "dailyprice-" + end_date + ".csv" 
get_daily_data(ts_api, start_date, end_date, file_reslult)