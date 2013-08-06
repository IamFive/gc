# -*- coding: utf-8 -*-
#
# Copyright (c) 2011-2013 Woo-cupid(iampurse#vip.qq.com)
#


HTTPS_ONLY = (100, 'Only can be access with https mode')
PARAM_ILLEGAL = (101, 'illegal parameter')

INVALID_JSON = (102, 'Could not parse json. Make sure to use double quotes and close all braces.')
INVALID_PAGINATE = (103, 'When paginate, limit should between 0 and 200 and page should be greate than 0')

RESOURCE_NOT_EXIST = (404, 'Resource is not exist')
RESOURCE_EXIST = (409, 'Resource duplicate')
