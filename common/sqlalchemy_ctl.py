#!/bin/env python
# -*- coding:utf8 -*-

from datetime import datetime
import time

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from common.my_log import logger
from conf import settings

Base = declarative_base()
connect_sql = ("mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8" %
               (settings.MYSQL_USER,
                settings.MYSQL_PWD,
                settings.MYSQL_HOST,
                settings.MYSQL_PORT,
                settings.MYSQL_DB))

if settings.DEBUG:
    engine = create_engine(
        connect_sql,
        encoding='utf-8',
        pool_recycle=settings.MYSQL_CONNECT_TIMEOUT,
        echo="debug",
        echo_pool="debug")
else:
    engine = create_engine(
        connect_sql,
        pool_recycle=settings.MYSQL_CONNECT_TIMEOUT,
        encoding='utf-8')

DBSession = sessionmaker(bind=engine, expire_on_commit=False)
