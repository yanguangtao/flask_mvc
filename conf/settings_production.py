#!/bin/env python
# -*- coding:utf8 -*-


class BaseConfig(object):
    DEBUG = False
    CREATE_TABLE = True

    MYSQL_HOST = "127.0.0.1"
    MYSQL_PORT = 3306
    MYSQL_USER = "root"
    MYSQL_PWD = "yan718844"
    MYSQL_DB = "mytest"

    # 本地运维平台redis信息
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379
    REDIS_DB = 1
    REDIS_PWD = ""

    # 3小时后自动重连mysql
    MYSQL_CONNECT_TIMEOUT = 3 * 60 * 60
