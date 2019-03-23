# coding=utf-8
__author__ = 'qwteng'

import tushare as ts
import requests


# get tushare api
def get_tsapi():
    ts.set_token("b84661efadd955c6eb9cea5a6a1b7ffe3e5a4831c2de7b7c2e8d2c01")
    return ts.pro_api()


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


# get real time price
def get_sina_source_realtime(code):
    BASIC_URL = 'http://hq.sinajs.cn/list='
    req = requests.get(BASIC_URL + code)
    text = req.text
    return text
