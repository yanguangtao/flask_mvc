#!/bin/env python
# -*-coding:utf-8-*-

from hashlib import sha1

import requests
from sqlalchemy import desc, inspect, func

from common.my_log import logger
from conf import settings


class BaseController(object):
    def __init__(self, model):
        self._model = model
        self.model = model

    def _clean_value(self, value):
        if isinstance(value, (str, unicode)):
            return value.strip()
        return value

    def _filter_value(self, kwargs):
        return filter(lambda x: (
            x != "metadata"
            and x != "id"
            and not x.startswith("_")
            and x in kwargs
        ), dir(self._model))

    def __encryption(self, value):
        # 明文sha1加密
        password = sha1(str(value).strip()).hexdigest()
        return password

    def do_filter(self, **kwargs):
        session = kwargs.get("session", None)
        if session is None:
            return None
        pk = kwargs.get("id", None)
        try:
            filter_obj = session.query(self._model)
            if pk is not None:
                return filter_obj.filter_by(id=pk)
            value = {k: self._clean_value(kwargs[k]) for k in self._filter_value(kwargs)}
            filter_obj = filter_obj.filter_by(**value)
            kv = kwargs.get("like", None)
            if kv is not None:
                k, v = kv.split("^")
                filter_obj = filter_obj.filter(getattr(self._model, k).like("%%%s%%" % v))
            id_list = kwargs.get("id_list", None)
            if id_list is not None:
                filter_obj = filter_obj.filter(getattr(self._model, "id").in_(id_list))
            filter_condition = kwargs.get('filter_condition', None)
            if filter_condition is not None:
                filter_obj = filter_obj.filter(filter_condition)
            return filter_obj
        except Exception as e:
            logger.error(u"查询%s出错. %s, %s" % (self._model.__tablename__, e, kwargs))
            return None

    def filter_item(self, **kwargs):
        session = kwargs.get("session", None)
        if session is None:
            return None, None
        start = int(kwargs.get("start", -1))
        end = int(kwargs.get("end", -1))
        compare_key = kwargs.get("compare_key", None)
        gte = kwargs.get("gte", None)
        gt = kwargs.get("gt", None)
        lte = kwargs.get("lte", None)
        lt = kwargs.get("lt", None)
        pk = kwargs.get("id", None)
        try:
            filter_obj = self.do_filter(**kwargs)
            if not filter_obj:
                return None, None
            if compare_key and hasattr(self._model, compare_key):
                if gte:
                    filter_obj = filter_obj.filter(getattr(self._model, compare_key) >= gte)
                if gt:
                    filter_obj = filter_obj.filter(getattr(self._model, compare_key) > gt)
                if lte:
                    filter_obj = filter_obj.filter(getattr(self._model, compare_key) <= lte)
                if lt:
                    filter_obj = filter_obj.filter(getattr(self._model, compare_key) < lt)
            if pk:
                return filter_obj.first(), 1
            order_by = kwargs.get("order_by", None)
            order_method = kwargs.get("order_method", None)
            if order_by is None:
                filter_obj = filter_obj.order_by(desc("id"))
            else:
                if order_method == "desc":
                    filter_obj = filter_obj.order_by(desc(order_by))
                else:
                    filter_obj = filter_obj.order_by(order_by)
            if start == -1 and end == -1:
                data = filter_obj.all()
                return data, len(data)
            else:
                pk = self.get_model_pk()
                if pk is None:
                    return None, None
                return filter_obj[start:end], filter_obj.with_entities(func.count(pk)).scalar()
        except Exception as e:
            logger.error(u"查询%s出错. %s, %s" % (self._model.__tablename__, e, kwargs))
            return None, None

    def new_item(self, **kwargs):
        session = kwargs.get("session", None)
        if session is None:
            return False
        try:
            value = {k: self._clean_value(kwargs[k]) for k in self._filter_value(kwargs)}
            if 'password' in value:
                # sha1加密密码字符
                value['password'] = self.__encryption(value['password'])
            new_obj = self._model(**value)
            session.add(new_obj)
            return new_obj
        except Exception as e:
            logger.error(u"新建%s出错. %s, %s" % (self._model.__tablename__, e, kwargs))
            return False

    def update_item(self, **kwargs):
        session = kwargs.get("session", None)
        if session is None:
            return False
        try:
            value = {k: self._clean_value(kwargs[k]) for k in self._filter_value(kwargs)}
            if 'password' in value:
                # sha1加密密码字符
                value['password'] = self.__encryption(value['password'])
            filter_obj = self.do_filter(**kwargs)
            if filter_obj:
                filter_obj.update(value)
                return True
            else:
                return False
        except Exception as e:
            logger.error(u"修改%s出错. %s, %s" % (self._model.__tablename__, e, kwargs))
            return False

    def delete_item(self, **kwargs):
        session = kwargs.get("session", None)
        if session is None:
            return False
        try:
            filter_obj = self.do_filter(**kwargs)
            if filter_obj:
                filter_obj.delete()
                return True
            else:
                return False
        except Exception as e:
            logger.error(u"删除%s出错. %s, %s" % (self._model.__tablename__, e, kwargs))
            return False

    def id_match(self, session, _input, match_key, attribute_list=None):
        """
        将ID匹配到对应的可读字段
        :param session:
        :param _input:
        :param match_key:
        :param attribute_list: [(当前存在的属性，新建的属性),
            当前存在的属性，默认把当前属性名字填充到新建属性里面
        ]
        :return: True/False
        """
        if session is None or attribute_list is None:
            return False
        if not isinstance(_input, list):
            input = [_input]
        else:
            input = _input
        id_list = [getattr(i, match_key) for i in input]
        item_list, _ = self.filter_item(session=session, id_list=id_list)
        # id_list 里面所有ID 都不匹配，返回None，直接结束函数。否则后面的id_dict中的for循环报错
        if item_list is None:
            return True
        id_dict = {getattr(k, "id"): k for k in item_list}
        for item in input:
            for i in attribute_list:
                if not isinstance(i, list) and not isinstance(i, tuple):
                    attribute, new_attribute = i, i
                else:
                    attribute, new_attribute = i[0], i[1]
                setattr(item, new_attribute, getattr(
                        id_dict.get(getattr(item, match_key), None),
                        attribute, None))
        return True

    def get_model_pk(self):
        """
        获取model主键
        :return: Column
        """
        try:
            ins = inspect(self.model)
            return ins.primary_key[0]
        except Exception as e:
            logger.error("获取主键失败e" % e)
            return None


