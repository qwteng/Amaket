# coding=utf-8
__author__ = 'qwteng'
import logging
from os.path import join
from data_source import get_tsapi
from sqlalchemy import create_engine
import pandas as pd
from data_source import get_tsapi
from init_env import *
from data_source import *


config_file = 'config.yaml'
sql_stock_tob_query = 'select * from t_stock_tob'


config = get_yaml_data(config_file)
logfile = config['logfile']
dbname = config['dbname']
print(config)

logger_init(logfile)
logging.info('start ...')
date='20190916'

engine = create_engine('sqlite:///' + dbname)
ts = get_tsapi()
df_tob = pd.read_sql(sql_stock_tob_query, engine)
df_tob_track = df_tob.copy()

df_tob_track['date'] = date
df_tob_track['close'] = pd.NaT
df_tob_track['premium'] = pd.NaT
rslt = df_tob_track
for index, row in df_tob_track.iterrows():
    code = row['code']
    price_tob = row['price_tob']
    df_price = ts.daily(ts_code=code,start_date='20190910', end_date=date)
    rslt = rslt.append(df_price)
    #rslt =  pd.concat([df_tob_track, df_price],axis=1,sort=False, join='outer')
    #price_close = df_price.iat[0, 5]
    #premium = pd.NaT
    #if price_tob != '':
    #    premium = round(price_close/price_tob - 1, 2) * 100
    #df_tob_track.iloc[index, 6] = price_close
    #df_tob_track.iloc[index, 7] = premium
print(rslt)
