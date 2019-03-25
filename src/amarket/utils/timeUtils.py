# coding=utf-8
__author__ = 'qwteng'
from datetime import datetime, timedelta
from multimethod import multimethod


DATE_FORMAT = '%Y%m%d'


@multimethod
def get_workday(date: datetime, flag: bool):
    weekday = date.weekday()
    date_wd = date
    # Saturday:5, Sunday:6
    if weekday == 5:
        if flag:
            offset_day = 2
        else:
            offset_day = -1
        date_wd = date + timedelta(days=offset_day)
    elif weekday == 6:
        if flag:
            offset_day = 1
        else:
            offset_day = -2
        date_wd = date + timedelta(days=offset_day) 

    return date_wd


@multimethod
def get_workday(date_str: str):
    datetime_input = datetime.strptime(date_str, DATE_FORMAT)
    date_wd = get_workday(datetime_input, False)
    return date_wd.strftime(DATE_FORMAT)


@multimethod
def get_workday(date: datetime, offset: int):
    date_wd = get_workday(date, False)
    flag = True
    if offset == 0:
        return date_wd
    elif offset > 0:
        remainder = offset % 5
    else:
        remainder = offset % -5   
        flag = False
    multiple = (int)(offset / 5)
    offset_wd = remainder + multiple * 7
    return get_workday(date_wd + timedelta(days=offset_wd), flag)

@multimethod
def get_workday(date_str: str, offset: int):
    datetime_input = datetime.strptime(date_str, DATE_FORMAT)
    date_wd = get_workday(datetime_input, offset)
    return date_wd.strftime(DATE_FORMAT)

