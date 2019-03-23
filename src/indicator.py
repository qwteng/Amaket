# coding=utf-8
__author__ = 'qwteng'
import time
import logging
from amarket.ds.data_source import *
from init_env import *
logfile = 'log.txt'
logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
        datefmt='%a, %d %b %Y %H:%M:%S',
        filename=logfile,
        filemode='w')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

ts_api = get_tsapi()
stocks = get_stock_basic(ts_api)
date = '20190322'
for row in stocks.itertuples(index=True, name='Pandas'):
    ts_code = getattr(row, 'ts_code')
    time.sleep(0.4)
    logging.info(ts_code)
    bar = ts_api.daily(ts_code=ts_code, start_date=date, end_date=date)
    if bar is None or bar.size<1:
        logging.warn(str(bar))
        continue
    change = bar.loc[0][ 'change']
    logging.info(ts_code + ', ' + str(change))
    if change > 9.0:
        logging.info('*******')
    