#!/bin/env python
# -*- coding: UTF-8 -*-

import redis

from .my_log import logger
from conf import settings


class Redis_db():

    def __init__(self, host='localhost', port=6379, db=0, pwd=None, socket_timeout=1):
        '''
        http://redis-py.readthedocs.org/en/latest/
        '''
        self.host = host
        self.port = port
        self.which_db = db
        self.pwd = pwd
        self.socket_timeout = socket_timeout
        self.db = None
        self.connect_db()

    def connect_db(self):
        self.db = None
        try:
            self.db = redis.StrictRedis(
                host=self.host,
                port=int(self.port),
                db=self.which_db,
                password=self.pwd,
                socket_timeout=self.socket_timeout,
                charset='utf-8'
            )
            return True
        except Exception as err:
            logger.error("connect redis error: %s" % err)
            return False

    def is_db_connected(self):
        try:
            if self.db.ping() == True:
                return True
            else:
                return False
        except Exception as err:
            logger.error("redis is disconnect, err info: %s" % err)
        return False

    def check_connect(self):
        if not self.is_db_connected():
            if not self.connect_db():
                logger.error("redis is disconnect !!")
                return False
        return True


redis_obj = Redis_db(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB,
        pwd=settings.REDIS_PWD)
