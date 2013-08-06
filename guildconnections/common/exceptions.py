# -*- coding: utf-8 -*-
#
# Copyright (c) 2011-2013 Woo-cupid(iampurse#vip.qq.com)
#

class FriendlyException(Exception):

    '''
        thrown when user do something wrong and the system want to lead the user to a error show page.
    '''

    def __init__(self, code, message):

        self.code = code;

        if isinstance(message, list):
            Exception.__init__(self, ';'.join(message))
            self.msg_list = message;
        else:
            Exception.__init__(self, message)
            self.msg_list = [];
            if message:
                self.msg_list.append(message)


    def add_message(self, message):
        self.msg_list.append(message);

    def message(self, message):
        self.msg_list = []
        if isinstance(message, list):
            self.msg_list = message
        else:
            self.msg_list.append(message);

    # shorter name, will remove from_error_code later
    @staticmethod
    def fec(error_code, *args):
        return FriendlyException.from_error_code(error_code, *args)

    @staticmethod
    def from_error_code(error_code, *args):
        error_message = error_code[1]
        if args:
            error_message = error_message.format(*args)
        return FriendlyException(error_code[0], error_message)



