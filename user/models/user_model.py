#!/bin/env python
# -*- coding:utf8 -*-

from sqlalchemy import Column, String, Integer, DateTime, text

from common.sqlalchemy_ctl import Base
from common.utility import create_table
from conf import settings


class UserModel(Base):
    __tablename__ = 'user'
    id = Column(Integer(), primary_key=True, autoincrement=True)
    name = Column(String(256), nullable=False, server_default='')
    password = Column(String(256), nullable=False, server_default='')
    avatar = Column(String(256), nullable=False, server_default='')
    create_time = Column(DateTime(), nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    # 更新时间
    update_time = Column(DateTime(), nullable=False,
                         server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))


if settings.CREATE_TABLE:
    create_table("user")
