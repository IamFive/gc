# -*- coding: utf-8 -*-
#
# Copyright (c) 2011-2013 Woo-cupid(iampurse#vip.qq.com)
#
import json
from functools import wraps
from flask.templating import render_template
from flask.globals import request, g, current_app
from guildconnections.common.web.json_encoder import MongoExtEncoder

class RenderFormat():

    HTML = 'HTML'
    JSON = 'JSON'
    JSONP = 'JSONP'

    DEFAULT = JSON
    choices = (HTML, JSON, JSONP)


class ContentType():
    JSON = 'application/json'
    JSONP = 'application/javascript'
    HTML = 'text/html'
    TEXT = 'text/plain'

TPL_NAME_KEY = '_TPL_NAME_KEY_'

def render_html(template=None):

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            ctx = f(*args, **kwargs)
            if ctx is None:
                ctx = {}
            elif not isinstance(ctx, dict):
                return ctx

            template_name = template
            if TPL_NAME_KEY in ctx:
                template_name = ctx[TPL_NAME_KEY]
            if template_name is None:
                template_name = request.endpoint.replace('.', '/') + '.html'

            return render_template(template_name, **ctx)
        return decorated_function

    return decorator


def render_json(only=None, exclude=None):

    def decorator(f):
        @wraps(f)
        def inner(*args, **kwargs):
#            try:
            view_result = f(*args, **kwargs)
            json_resp = JsonResp.make_success_resp(view_result);
#            except Exception, e:
#                json_resp = JsonResp.make_failed_resp(500, e.message);
            return current_app.response_class(
                json.dumps(json_resp,
                           default=MongoExtEncoder(only, exclude).default,
                           indent=None if request.is_xhr else 2),
                mimetype='application/json'
            );
        return inner

    return decorator

def render_jsonp(only=None, exclude=None):
    """Wraps JSONified output for JSONP requests."""

    def decorator(f):
        @wraps(f)
        def inner(*args, **kwargs):
            view_result = f(*args, **kwargs)
            json_resp = JsonResp.make_success_resp(view_result);
            jsonp_resp = json.dumps(json_resp,
                           default=MongoExtEncoder(only, exclude).default,
                           indent=None if request.is_xhr else 2)
            callback = request.args.get('callback', False)
            if callback:
                content = str(callback) + '(' + jsonp_resp + ')'
                mimetype = 'application/javascript'
                return current_app.response_class(content, mimetype=mimetype)
            else:
                return jsonp_resp
        return inner

    return decorator


def smart_render(**decorator_kwargs):

    def decorator(f):

        @wraps(f)
        def inner(*args, **kwargs):

            template = decorator_kwargs['template'] if 'template' in decorator_kwargs else None
            only = decorator_kwargs['only'] if 'only' in decorator_kwargs else None
            exclude = decorator_kwargs['exclude'] if 'exclude' in decorator_kwargs else None

            if g.rformat == RenderFormat.JSON:
                return render_json(only=only, exclude=exclude)(f)(*args, **kwargs);
            if g.rformat == RenderFormat.JSONP:
                return render_jsonp(only=only, exclude=exclude)(f)(*args, **kwargs);
            elif g.rformat == RenderFormat.HTML:
                return render_html(template)(f)(*args, **kwargs);

        return inner

    return decorator;

class JsonResp(object):
    """ common JSON response factory. """

    @staticmethod
    def make_default_resp():
        return {}

    @staticmethod
    def make_success_resp(result=None):
        resp = dict(result='')
        if result != None:
            resp['result'] = result
        return resp

    @staticmethod
    def make_failed_resp(error_code='', error_msg='', result=None):
        resp = dict(error_code='', error_msg='')
        resp['error_code'] = error_code
        resp['error_msg'] = error_msg
        if result:
            resp['result'] = result
        return resp

    @staticmethod
    def from_error_code(error_code):
        resp = dict(error_code='', error_msg='')
        resp['error_code'] = error_code[0]
        resp['error_msg'] = error_code[1]
        return resp

