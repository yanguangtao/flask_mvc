#!/bin/env python
# -*-coding:utf-8-*-


from common.base_controller import BaseController
from user.models import UserModel


class UserController(BaseController):
    def check_update_items(self, session, user_id):
        data, _ = user_ctl.filter_item(session=session, id=user_id)
        if data:
            return True
        return False

user_ctl = UserController(UserModel)

