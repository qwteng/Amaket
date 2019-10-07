# coding=utf-8
__author__ = 'qwteng'

import tushare as ts
import requests


# get tushare api
def get_tsapi():
    ts.set_token("b84661efadd955c6eb9cea5a6a1b7ffe3e5a4831c2de7b7c2e8d2c01")
    return ts.pro_api()


# get stock daily price
def get_stock_daily(ts_api, code, start_date, end_date):
    pass


# get stock basic info to dataframe
def get_stock_basic(ts_api):
    df_stock_basic = ts_api.query(
        'stock_basic',
        excjamge_id='',
        list_status='L',
        fields='ts_code, symbol, name, area, industry, list_date, market,is_hs'
    )
    return df_stock_basic


# get top 10 holders info to dataframe
def get_top10_holders(ts_api, ts_code, start_date, end_date):
    df_top10_holder = ts_api.query(
        'top10_holders',
        ts_code=ts_code,
        start_date=start_date,
        end_date=end_date)
    return df_top10_holder


# get top 10 float holders info to dataframe
def get_top10_floatholders(ts_api, ts_code, start_date, end_date):
    df_top10_floatholder = ts_api.query(
        'top10_floatholders',
        ts_code=ts_code,
        start_date=start_date,
        end_date=end_date)
    return df_top10_floatholder


#
def get_quater_range(quater):
    quater_map = {
        'Q1': ('0101', '0330'),
        'Q2': ('0401', '0630'),
        'Q3': ('0701', '0930'),
        'Q4': ('1001', '1231')
    }
    return quater_map.get(quater)


class StockPrice:
    def __init__(self):
        self.code = ""
        self.name = ""
        self.open = 0.0
        self.lastclose = 0.0
        self.present = 0.0
        self.high = 0.0
        self.low = 0.0

    def to_str(self):
        map = {}
        map['code'] = self.code
        map['name'] = self.name
        map['open'] = self.open
        map['lastclose'] = self.lastclose
        map['present'] = self.present
        map['high'] = self.high
        map['low'] = self.low
        return str(map)


def sina_realtime_to_stockprice(text):
    elems = text.split(',')
    name = elems[0].split('="')[1]
    open = elems[1]
    lastclose = elems[2]
    present = elems[3]
    high = elems[4]
    low = elems[5]
    stockPrice = StockPrice()
    stockPrice.name = name
    stockPrice.open = open
    stockPrice.lastclose = lastclose
    stockPrice.present = present
    stockPrice.high = high
    stockPrice.low = low
    return stockPrice


# get real time price
def get_sina_source_realtime(code):
    BASIC_URL = 'http://hq.sinajs.cn/list='
    req = requests.get(BASIC_URL + code)
    text = req.text
    stockPrice = sina_realtime_to_stockprice(text)
    return stockPrice