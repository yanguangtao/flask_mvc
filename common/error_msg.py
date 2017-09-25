#!/bin/env python
# -*- coding:utf8 -*-

SUCCESS = 0, ""
SERVER_ERROR = 1, u"服务器异常"
SESSION_ERROR = 2, u"登录过期"
PARAMS_ERROR = 3, u"参数错误"
NEW_ACCOUNT_ERROR = 4, u"用户名重复"
EMAIL_NAME_ERROR = 5, u"用户名非法"
PWD_ERROR = 6, u"密码错误"
OLD_PWD_ERROR = 7, u"旧密码错误"
VALUE_ERROR = 8, u'获取参数值错误'
DATABASES_ERROR = 9, u'数据库写入失败'
DATABASE_DELETE_ERROR = 10, u'数据删除失败'
USER_NOT_EXIST = -1, u'用户不存在'

RET_CODE_MAP = { 
    0: 200,
    1: 500,
    3: 501
}
