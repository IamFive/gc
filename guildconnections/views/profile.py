# -*- coding: utf-8 -*-
#
# @author: Five
# Created on 2013-5-24
#
from flask.blueprints import Blueprint
from flask.globals import g, request, current_app
from flask_login import current_user
from guildconnections.common.tools.utils import mkdirs
from guildconnections.common.web.renderer import smart_render
from guildconnections.constants import DEFAULT_RENDER_EXCLUDE
from guildconnections.models import User, GamerForm, Game
import os
from guildconnections.uploads import Avatars
from mongoengine.errors import NotUniqueError
from guildconnections.common.exceptions import FriendlyException
from guildconnections import error_code

bp_profile = Blueprint('profile', __name__)

exclude = list(DEFAULT_RENDER_EXCLUDE)
exclude.extend(('password', 'verify_code'))

@bp_profile.route('/me', methods=['GET'])
@smart_render(exclude=exclude)
def me():
    """ get logined user detail info """
    return current_user.get()


@bp_profile.route('/gamer', methods=['POST', 'PUT'])
@smart_render(exclude=exclude)
def add_gamer_profile():
    """ add gamer profile for current user """
    user_id = current_user.get().id
    user = User.objects.get_or_404(id=user_id)

    # should we validate object_id here?

    # auto populate with g.formdata
    game_form = GamerForm(g.formdata)
    game_form.populate_obj(user.gamer)

    if request.files and request.files['avatar']:
        filename = Avatars.save(request.files['avatar'])
        user.gamer.avatar = Avatars.url(filename)

    # manually handle games
    user.gamer.games = [Game(id=_id)
                        for _id in request.form.getlist('games')]

    user.save()
    return user


# def allowed_file(filename):
#    return '.' in filename and \
#           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


