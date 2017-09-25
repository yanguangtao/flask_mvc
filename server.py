#!/bin/env python
# -*-coding:utf-8-*-

import importlib

from flask import Flask, url_for
from flask_script import Manager, Shell, Server

from common.sqlalchemy_ctl import DBSession

import restful_urls


app = Flask(__name__, static_url_path='/static')


def dispatch(item):
    def _dispatch(**kwargs):
        obj = item[1]
        kwargs["controller_obj"] = item[2]
        return obj(**kwargs).dispatch()
    return _dispatch

methods = ["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS"]

for i in restful_urls.urls:
    _methods = methods
    if len(i) == 4:
        _methods = i[3]
    url_prefix = "/%s" % i[0]
    app.add_url_rule(url_prefix, url_prefix, dispatch(i), methods=_methods)


def _make_shell_context():
    return {'app': app, 'dbsession': DBSession()}

manager = Manager(app)
manager.add_command("shell", Shell(make_context=_make_shell_context))
manager.add_command("runserver", Server(host="0.0.0.0", port=7789, use_debugger=True))


if __name__ == '__main__':
    manager.run()
