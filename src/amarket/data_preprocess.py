# coding=utf-8
__author__ = 'qwteng'
import time
import pandas as pd
from amarket.ds.data_source import get_stock_basic


def get_daily_data(ts_api, start_date, end_date, file_reslult):
    stocks = get_stock_basic(ts_api)
    bars = []
    codes = []
    for row in stocks.itertuples(index=True, name='Pandas'):
        ts_code = getattr(row, 'ts_code')
        time.sleep(0.4)
        bar = ts_api.daily(ts_code=ts_code, start_date=start_date, end_date=end_date)
        if bar is None or bar.size < 1:
            continue
        codes.append(ts_code)
        bars.append(bar)
    data = pd.concat(bars, codes)
    data.to_csv(file_reslult)
