# -*- coding: utf-8 -*-
#
# @author: Five
# Created on 2013-5-14
#
from flask.blueprints import Blueprint
from flask.globals import g
from flask_login import login_user, logout_user
from guildconnections import error_code
from guildconnections.common.exceptions import FriendlyException
from guildconnections.common.flask_login_ext import SessionUserMixin
from guildconnections.common.interceptors import no_auth_required
from guildconnections.common.web.renderer import smart_render
import datetime
import random
import string
from guildconnections.models import User
from mongoengine.errors import NotUniqueError

bp_auth = Blueprint('authorize', __name__)

@no_auth_required()
@bp_auth.route('/signup', methods=['post', 'get'])
@smart_render()
def signup():
    ''' signup user. '''
    email = g.formdata.get('email')
    name = g.formdata.get('name')
    password = g.formdata.get('password')

    # validate input
    if not email or not name or not password:
        raise FriendlyException.fec(error_code.ENP_REQUIRED)

    # generate a verify code.
    verify_code = ''.join(random.sample(string.letters, 6))
    user = User(email=email, name=name, password=password,
                verify_code=verify_code)
    try:
        user.save()
    except NotUniqueError:
        raise FriendlyException.fec(error_code.EMAIL_DUPLICATE, email)
    # should we send a email here?
    return user


@bp_auth.route('/login', methods=['POST'])
@no_auth_required()
@smart_render()
def login():

    email = g.formdata.get('email')
    password = g.formdata.get('password')
    user = User.objects(email=email, password=password).first()

    remember = (g.formdata.get('remember', 'no') == 'yes')
    if user is not None:
        if login_user(SessionUserMixin(user), remember=remember):
            user.last_login_on = datetime.datetime.now()
            user.save()
            return True

    raise FriendlyException.fec(error_code.LOGIN_FAILED)


@bp_auth.route('/logout', methods=['GET'])
@smart_render()
def logout():
    logout_user()
    return True

