import os, sys
from utils import get_tsapi, get_non_tradable_stick_price_info, get_yaml_data
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import click
from flask_cli import FlaskCLI
from utils import *
import pandas as pd

app = Flask(__name__)
FlaskCLI(app)
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

config_file = 'config.yaml'
config = get_yaml_data(config_file)
logfile = config['logfile']
dbname = config['dbname']

app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, dbname)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Price(db.Model):
    ts_code = db.Column(db.String(9),primary_key=True)
    trade_date = db.Column(db.String(8),primary_key=True)
    open = db.Column(db.Float)
    high = db.Column(db.Float)
    low = db.Column(db.Float)
    close = db.Column(db.Float)
    pre_close = db.Column(db.Float)
    change = db.Column(db.Float)
    pct_chg = db.Column(db.Float)


class Tob(db.Model):
    ts_code = db.Column(db.String(9), primary_key=True)
    tob_date = db.Column(db.String(8), primary_key=True)
    price = db.Column(db.Float)
    amount = db.Column(db.Float)


@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    """Initialize the database."""
    if drop:  # 判断是否输入了选项
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')  # 输出提示信息


@app.cli.command()
def get():
    #click.echo('start to get data')
    ts = get_tsapi()
    df_tob = pd.read_sql_table('tob', db.engine)
    df_tob['tob_date'] = df_tob['tob_date'].astype(object)
    print(df_tob.dtypes)
    df = None
    for index, row in df_tob.iterrows():
        ts_code = row['ts_code']
        date = str(row['tob_date'])
        if df is None:
            df = get_non_tradable_stick_price_info(ts, ts_code, date)
        else:
            df = df.append(get_non_tradable_stick_price_info(ts, ts_code, date))
    if df is None:
        return
    df_price = df[['ts_code','trade_date', 'open', 'high', 'low', 'close', 'pre_close', 'change', 'pct_chg']]
    print(df_price)
    pd.io.sql.to_sql(df_price, 'price', db.engine, index=None, if_exists='replace')

    click.echo('get data over')


@app.cli.command()
def gettob():
    click.echo('start to get tob')
    df = pd.read_csv('tob.csv')
    pd.io.sql.to_sql(df, 'tob', db.engine, index=None, if_exists='replace')
    print(df)
    click.echo('get tob over')
