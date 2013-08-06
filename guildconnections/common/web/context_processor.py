# -*- coding: utf-8 -*-
#
# Copyright (c) 2011-2013 Woo-cupid(iampurse#vip.qq.com)
#
from flask.globals import current_app

def utility_processor():

    def url_for_upload(relative=''):
        relative = str(relative).lstrip('/')
        return '/'.join([current_app.config['MEDIA_URL_PATH'], current_app.config['UPLOAD_FOLDER_NAME'], relative])

    def url_for_appicon(relative=''):
        return '/'.join([url_for_upload(), current_app.config['APP_ICON_FOLDER_NAME'], relative])

    return dict(url_for_upload=url_for_upload, url_for_appicon=url_for_appicon)
