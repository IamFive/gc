# -*- coding: utf-8 -*-
#
# Copyright (c) 2011-2013 Woo-cupid(iampurse#vip.qq.com)
#
# @author: Five
# Created on 2013-2-24
#
from guildconnections.common.exceptions import FriendlyException
from guildconnections.common import error_code
from functools import wraps

def reraise(to_raise):

    def decorator(f):
        @wraps(f)
        def inner(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except:
                raise to_raise
        return inner

    return decorator;

@reraise(FriendlyException.from_error_code(error_code.INVALID_JSON))
def is_object_id(object_id_value):
    from bson.objectid import ObjectId
    ObjectId(unicode(object_id_value))
    return True

@reraise(FriendlyException.from_error_code(error_code.INVALID_JSON))
def is_json(json_value):
    import json
    return json.loads(json_value)

