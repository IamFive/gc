# -*- coding: utf-8 -*-
#
# Copyright (c) 2011-2013 Woo-cupid(iampurse#vip.qq.com)
#

import os
import json
import logging

from guildconnections.constants import ROOT, STATIC_URL_PATH
from guildconnections.common.exceptions import FriendlyException
from guildconnections.common.interceptors import setup_render_as_interceptor
from guildconnections.common.flask_login_ext import load_user
from guildconnections.common.interceptors import setup_formdata_interceptor
from guildconnections.common.interceptors import no_auth_required, setup_auth_interceptor
from guildconnections.common.web.renderer import smart_render, JsonResp, RenderFormat, ContentType
from guildconnections.common.web.context_processor import utility_processor

from flask_mongoengine import MongoEngine
from mongoengine.connection import get_db
from flask import Flask, render_template, request
from flask import make_response
from flask_login import LoginManager

from logging import Formatter, FileHandler
from logging.handlers import TimedRotatingFileHandler
from flask.helpers import url_for
from flask.globals import current_app, g
from flask.wrappers import Response

from werkzeug.utils import redirect
from werkzeug.wsgi import SharedDataMiddleware
from guildconnections import version_context_processor
from guildconnections.common.tools.env import ResourceLoader
from guildconnections.common import error_code
from flaskext.uploads import configure_uploads
from guildconnections.uploads import Avatars
from guildconnections.common.tools.utils import mkdirs
from mongoengine.errors import ValidationError
from pymongo.errors import PyMongoError

app = None;

def init_mongo_engine():
    app.mongo_db = MongoEngine(app)

def init_logger():

    log_format = app.config.get('LOG_FORMAT')
    if app.config.get('LOG_FORMAT'):
        app.debug_log_format = log_format;

    # setup root log format - global filter.
    app.logger.setLevel(app.config.get('LOGGER_ROOT_LEVEL'))
    log_file_folder = app.config.get('FILE_LOG_HANDLER_FODLER')
    mkdirs(log_file_folder, is_folder=True)

    filename = os.path.join(log_file_folder, app.import_name + '.log')
    file_handler = TimedRotatingFileHandler(filename=filename, when="midnight",
                                            backupCount=10)
    file_handler.suffix = "%Y%m%d"
    file_handler.setLevel(app.config.get('FILE_LOG_HANDLER_LEVEL'))
    file_handler.setFormatter(Formatter(log_format))
    app.logger.addHandler(file_handler)


def init_bp_modules():
    """add blueprint modules.
    """
    global app

    from guildconnections.views.authorize import bp_auth
    app.register_blueprint(bp_auth, url_prefix='/api/authorize')

    from guildconnections.views.profile import bp_profile
    app.register_blueprint(bp_profile, url_prefix='/api/profile')

    from guildconnections.views.guides import bp_guide
    app.register_blueprint(bp_guide, url_prefix='/api/guilds')

    @app.route('/api/version', methods=['GET', 'POST'])
    @no_auth_required()
    @smart_render()
    def version_handler():
        from guildconnections import version
        return version()


def init_login_manager():
    login_manager = LoginManager()
    login_manager.setup_app(app)
    login_manager.user_callback = load_user

def init_jinja_env():
    app.context_processor(utility_processor)
    app.context_processor(version_context_processor)


def init_error_handler():


    def handler_ex(ex, status=400):

        status = ex.code if ex.code >= 400 and ex.code < 500 else 400

        if g.rformat == RenderFormat.HTML:
            return render_template('{}.html'.format(status), error=ex), status

        if isinstance(ex, FriendlyException) and len(ex.msg_list) == 1:
            message = ex.msg_list[0]
        else:
            message = ex.msg_list
        resp = json.dumps(JsonResp.make_failed_resp(ex.code, message))

        if g.rformat == RenderFormat.JSON:
            return Response(resp, mimetype=ContentType.JSON), status
        elif g.rformat == RenderFormat.JSONP:
            callback = request.args.get('callback', False)
            if callback:
                content = "{}({})".format(callback, resp)
                return Response(content, mimetype=ContentType.JSONP,
                                status=200)
            return Response(resp, mimetype=ContentType.JSON, status=200)


    @app.errorhandler(404)
    def page_not_found(error):
        ex = FriendlyException.fec(error_code.RESOURCE_NOT_EXIST)
        return handler_ex(ex, 404)

    @app.errorhandler(FriendlyException)
    def friendly_ex_handler(ex):
        status = ex.code if ex.code >= 400 and ex.code < 500 else 400
        return handler_ex(ex, status=status)

    @app.errorhandler(ValidationError)
    def form_validata_ex_handler(error, status=400):
        ex = FriendlyException(400, error.to_dict())
        return handler_ex(ex, status)

    @app.errorhandler(PyMongoError)
    def mongo_op_ex_handler(error, status=400):
        ex = FriendlyException(400, str(error))
        return handler_ex(ex, status)

    @app.errorhandler(Exception)
    def exception_handler(error, status=400):
        ex = FriendlyException(400, str(error))
        return handler_ex(ex, status)


def init_interceptors():
    setup_render_as_interceptor(app)
    setup_auth_interceptor(app)
    setup_formdata_interceptor(app)


def setup_flask_initial_options():

    static_folder = ResourceLoader.get().configs.get('STATIC_FOLDER')
    template_folder = ResourceLoader.get().configs.get('TEMPLATE_FOLDER')
    if not static_folder:
        static_folder = os.path.join(ROOT, 'static')

    if not template_folder:
        template_folder = os.path.join(ROOT, 'templates')

    options = dict(static_url_path=STATIC_URL_PATH)
    options['static_folder'] = static_folder
    options['template_folder'] = template_folder
    return options


def init_uploads():
    from guildconnections.uploads import upload_list
    configure_uploads(app, upload_list)


def startup_app():

    # initial settings first, or change to use confd like curupira?
    global app

    if not app:
        args = setup_flask_initial_options()
        app = Flask('guildconnections', **args)

        app.config.update(ResourceLoader.get().configs)
        app.debug = app.config.get('DEBUG', False)

        init_logger()

        try:
            init_mongo_engine()
            init_jinja_env()
            init_error_handler()
            init_login_manager()
            init_interceptors()
            init_bp_modules()
            init_uploads()
            app.logger.info('Start success from ROOT [%s] .', ROOT)
        except Exception, e:
                app.logger.error('Start gc faild!')
                app.logger.exception(e)
                raise e
    return app

def init_db():
    with current_app.app_context():
        folder_name = app.config.get('INIT_DATA_FOLDER_NAME')
        folder_path = ResourceLoader.get().get_resoure(folder_name).path
        if folder_path and os.path.isdir(folder_path):
            for data_file in os.listdir(folder_path):
                with open(folder_path + os.path.sep + data_file, 'r') as mqls:
                    get_db().eval(mqls.read())

def clear_db():
    with current_app.app_context():
        get_db().eval('db.dropDatabase()')
