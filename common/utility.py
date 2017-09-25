#!/bin/env python
# -*-coding:utf-8-*- 

import re
import datetime
import hashlib
import time
import traceback
import requests
from decimal import Decimal
from flask import jsonify
from IPy import IP
from sqlalchemy.ext.declarative import DeclarativeMeta

from conf import settings
from common.my_log import logger
from sqlalchemy_ctl import Base
from sqlalchemy_ctl import DBSession
from sqlalchemy_ctl import engine

def create_table(table_name=""):
    if table_name == "":
        Base.metadata.create_all(engine)
    else:
        Base.metadata.tables[table_name].create(bind=engine, checkfirst=True)


def drop_table(table_name=""):
    if table_name == "":
        Base.metadata.drop_all(engine)
    else:
        Base.metadata.tables[table_name].drop(bind=engine, checkfirst=True)


def to_dict_obj(
        orm_obj,
        need_fields=None,
        without_fields=None,
        datetime_format="%Y-%m-%d"):
    if isinstance(orm_obj, list):
        return [to_dict_obj(i, need_fields, without_fields, datetime_format) for i in orm_obj]
    elif isinstance(orm_obj.__class__, DeclarativeMeta):
        attr_dict = dict()
        for attr in [x for x in dir(orm_obj) if not x.startswith('_') and x != 'metadata']:
            data = getattr(orm_obj, attr)
            if need_fields and attr not in need_fields:
                continue
            if without_fields and attr in without_fields:
                continue
            if isinstance(data, datetime.datetime):
                attr_dict[attr] = data.strftime(datetime_format)
                if attr_dict[attr] == "1970-01-01":
                    attr_dict[attr] = ""
            elif isinstance(data, datetime.date):
                attr_dict[attr] = data.strftime("%Y-%m-%d")
            elif isinstance(data, datetime.timedelta):
                attr_dict[attr] = ((datetime.datetime.min + data).time().
                                   strftime("%Y-%m-%d %H:%M:%S"))
            elif isinstance(data, Decimal):
                attr_dict[attr] = float(data)
            else:
                attr_dict[attr] = data
        return attr_dict
    else:
        return orm_obj