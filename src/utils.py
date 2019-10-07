# coding=utf-8
__author__ = 'qwteng'

import tushare as ts
import requests
import logging
from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

import arrow


# common func

PLATE_CODE = {
    '600': 'SH',
    '601': 'SH',
    '603': 'SH',
    '688': 'SH',
    '000': 'SZ',
    '002': 'SZ',
    '300': 'SZ'
}


def get_yaml_data(yaml_file):
    file = open(yaml_file, 'r', encoding='utf-8')
    file_data = file.read()
    file.close()
    data = load(file_data, Loader=Loader)
    return data


def logger_init(logfile):
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
        datefmt='%a, %d %b %Y %H:%M:%S',
        filename=logfile,
        filemode='w')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)


def stock_code_standardize(code):
    if len(code) < 6:
        return None
    plate_code = PLATE_CODE[code[0:3]]
    return code[0:6] + '.' + plate_code


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


# desterilization of non-tradable shares
def get_non_tradable_stick_price_info(ts_api, code, date):
    code = stock_code_standardize(code)
    start_date = arrow.get(date).shift(days=-20).format('YYYYMMDD')
    end_date = arrow.get(date).shift(days=20).format('YYYYMMDD')
    df = ts_api.query('daily', ts_code=code, start_date=start_date, end_date=end_date)
    if df is None or df.size == 0:
        return None

    df_date = df[df.trade_date == date]
    if df_date.size == 0:
        return None
    df_date_loc = df_date.index.max()
    df_min_loc = df.index.min()
    df_nax_loc = df.index.max()
    min_loc = max(df_date_loc-7, df_min_loc)
    max_loc = min(df_date_loc+7, df_nax_loc)
    return df[min_loc:max_loc]


# get tender offer
def get_tob_price_info():
    pass
