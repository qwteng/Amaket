# coding=utf-8
__author__ = 'qwteng'
import logging
from init_env import logger_init
from data_source import get_sina_source_realtime


logger_init('app.log')
logging.info('start ...')
r = get_sina_source_realtime('sh204001')
print(r.to_str())
r = get_sina_source_realtime('sh511990')
print(r.to_str())

