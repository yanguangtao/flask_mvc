# -*-coding:utf-8-*-
from user.controllers import user_ctl
from user.views.user_view import User

urls = [
    ("user", User, user_ctl, ["GET", "POST"]),
]
