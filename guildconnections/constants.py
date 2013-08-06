# -*- coding: utf-8 -*-
#
# Copyright (c) 2011-2013 Woo-cupid (iampurse#vip.qq.com)
#

import os
ROOT = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.abspath(os.path.join(ROOT, '..'))

STATIC_URL_PATH = '/static'

DEFAULT_FORM_EXCLUDE = ('id', 'created_by', 'modified_by', 'created', 'modified', '_cls', '_types', 'status')
DEFAULT_RENDER_EXCLUDE = ('created_by', 'modified_by', 'created', 'modified')
