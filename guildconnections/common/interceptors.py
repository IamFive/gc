# -*- coding: utf-8 -*-
#
# Copyright (c) 2011-2013 Woo-cupid(iampurse#vip.qq.com)
#
from flask.globals import request, current_app, g
from flask_login import current_user
from guildconnections.common.tools.utils import get_formdata
from guildconnections.common.web.renderer import RenderFormat
import json
import os.path

def no_auth_required():
    def wrapper(func):
        func.__no_auth_required__ = True
        return func
    return wrapper


def setup_auth_interceptor(app):

    @app.before_first_request
    def init_no_auth_required_list():
        '''
            setup no authorize required resource list.
        '''
        if not hasattr(app, 'auth_exclude'):

            app.logger.info('setup no authorize resource list before first request.')

            urls = [path[1:] for path in app.config['RAW_RESOURCE_PATH']]
            app.auth_exclude = {
                'urls' : urls,
                'endwiths':app.config['RAW_RESOURCE_ENDWITH'],
                'endpoints' : [],
            };

            for key in app.view_functions.keys():
                if hasattr(app.view_functions[key], '__no_auth_required__') and getattr(app.view_functions[key], '__no_auth_required__'):
                    app.auth_exclude['endpoints'].append(key);

            app.logger.info('no authorize resource list is: ' + json.dumps(app.auth_exclude, indent=4))

    def required_login():
        path = request.path
        endpoint = request.endpoint
        root, ext = os.path.splitext(path)
        path_part1 = root.split('/')[1];
        return ((ext not in current_app.auth_exclude['endwiths']) and
                (path_part1 not in current_app.auth_exclude['urls']) and
                (endpoint not in current_app.auth_exclude['endpoints']))

    @app.before_request
    def before_request():
        if required_login() and not current_user.is_authenticated():
            return current_app.login_manager.unauthorized()

    @app.after_request
    def after_request(response):
        return response

def setup_formdata_interceptor(app):

    def inject_formdata():
        g.formdata = get_formdata(request)

    app.before_request(inject_formdata)

def setup_render_as_interceptor(app):
    """
        depend on setup_formdata_interceptor
    """

    from string import upper

    def inject_resp_type():

        def set_rf(rf_choice, default):
            rformat = upper(get_formdata(request).get('rformat', default));
            g.rformat = rformat if (rformat in rf_choice) else default

        set_rf(RenderFormat.choices, RenderFormat.DEFAULT)

    app.before_request(inject_resp_type)

