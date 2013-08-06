# -*- coding: utf-8 -*-
#
# Copyright (c) 2011-2013 Woo-cupid(iampurse#vip.qq.com)
#

METHOD = ('GET', 'POST', 'PUT', 'DELTE', 'ANY')

class Gender(object):
    M = ('M', 'Male')
    F = ('F', 'Female')
    U = ('U', 'Unknown')
    choices = (M, F, U)

class DataSource(object):
    GETCLEVER = 'GetClever'
    SYSTEM = 'System'
    choices = (GETCLEVER, SYSTEM)

class Status(object):
    INVALID = 0
    VALID = 1
    choices = (VALID, INVALID)
