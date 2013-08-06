# -*- coding: utf-8 -*-
#
# Copyright (c) 2011-2013 Woo-cupid(iampurse#vip.qq.com)
#

import os
from guildconnections.constants import ROOT, STATIC_URL_PATH

#------------- Application setting here. ---------------------

DEBUG = False
CSRF_ENABLED = False
SECRET_KEY = 'i am really not a secret key'

MEDIA_URL_PATH = '/m'
MEDIA_FOLDER = os.path.join(ROOT, 'medias')

INIT_DATA_FOLDER_NAME = 'init-mqls'


MONGODB_HOST = '127.0.0.1'
MONGODB_DB = 'gc'


LOGGER_ROOT_LEVEL = 'DEBUG'
FILE_LOG_HANDLER_FODLER = os.path.join(ROOT, 'logs')
FILE_LOG_HANDLER_LEVEL = 'DEBUG'
LOG_FORMAT = (
    '[%(asctime)s] %(levelname)s *%(pathname)s:%(lineno)d* : %(message)s'
)

# REST_API_DOMAIN = 'www.api.com'
RAW_RESOURCE_PATH = [MEDIA_URL_PATH, STATIC_URL_PATH]
RAW_RESOURCE_ENDWITH = ['.css', '.js', '.jpg', '.ico', '.png']


# UPLOADED_FILES_DEST = MEDIA_FOLDER
# UPLOADED_FILES_URL = MEDIA_URL_PATH
# UPLOADED_FILES_ALLOW
# UPLOADED_FILES_DENY
UPLOADS_DEFAULT_DEST = MEDIA_FOLDER
UPLOADS_DEFAULT_URL = MEDIA_URL_PATH

