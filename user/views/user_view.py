#!/bin/env python
# -*-coding:utf-8-*-

from flask import render_template
from sqlalchemy import or_

from common.base_view import BaseView
from common import error_msg
from common.my_log import logger
from common.utility import to_dict_obj


class User(BaseView):
    def get(self):
        try:
            data, total = self._controller_obj.filter_item(**self._input)
            self._data["total"] = total
            self._data["list"] = to_dict_obj(data)
            self._db_session.commit()
        except Exception as e:
            logger.error(u'查询user表失败: %s' % e)
            self._ret, self._msg = error_msg.SERVER_ERROR
            self._db_session.rollback()
        return self._response()

    def post(self):
        return super(User, self).post()

    def put(self):
        check_exist = self._controller_obj.check_update_items(**self._input)
        if not check_exist:
            self._ret, self._msg = error_msg.USER_NOT_EXIST
            return self._response()
        return super(User, self).put()

    def delete(self):
        return super(User, self).delete()

    # 访问网页url加action
    def get_action_list(self):
        return render_template("/user/user_list.html", **locals())
