# -*- coding: utf-8 -*-
#
# Copyright (c) 2011-2013 Woo-cupid(iampurse#vip.qq.com)
#
from flask_login import UserMixin
from guildconnections.models import User

class SessionUserMixin(UserMixin):

    def __init__(self, user):
        if user:
            self.orignal = user

    @property
    def id(self):
        return self.orignal.id

    @property
    def email(self):
        return self.orignal.email

    @property
    def status(self):
        return self.orignal.status

    def get(self):
        return self.orignal

    def is_active(self):
        return self.status == 1


def load_user(user_id):
    return SessionUserMixin(User.objects(id=user_id).first())
