# -*- coding: utf-8 -*-
#
# @author: Five
# Created on 2013-5-24
#
from flask.blueprints import Blueprint
from guildconnections.common.web.renderer import smart_render
from guildconnections.constants import DEFAULT_RENDER_EXCLUDE
from guildconnections.models import Guide, GuideForm
from flask.globals import g, request
from guildconnections.uploads import Logos

bp_guide = Blueprint('guide', __name__)


def save_or_update(guide, formdata=None):

    guide_form = GuideForm(formdata or g.formdata)
    guide_form.populate_obj(guide)
    guide.save()

    # save logo only when re-upload
    if request.files and request.files['logo']:
        filename = Logos.save(request.files['logo'])
        guide.logo = Logos.url(filename)

    return guide


@bp_guide.route('/', methods=['POST'])
@smart_render(exclude=DEFAULT_RENDER_EXCLUDE)
def create_guide():
    return save_or_update(Guide())


@bp_guide.route('/<guide_id>', methods=['PUT'])
@smart_render(exclude=DEFAULT_RENDER_EXCLUDE)
def update_guide(guide_id):
    guide = Guide.objects.get_or_404(id=guide_id)
    return save_or_update(guide)


@bp_guide.route('/<guide_id>', methods=['DELETE'])
@smart_render(exclude=DEFAULT_RENDER_EXCLUDE)
def delete_guide(guide_id):
    guide = Guide.objects.get_or_404(id=guide_id)
    guide.delete()
    return True


@bp_guide.route('/', methods=['GET'])
@smart_render(exclude=DEFAULT_RENDER_EXCLUDE)
def get_guide_list():
    paginate = Guide.objects.paginate(
        exclude=DEFAULT_RENDER_EXCLUDE
    )
    return paginate


@bp_guide.route('/<guide_id>', methods=['GET'])
@smart_render(exclude=DEFAULT_RENDER_EXCLUDE)
def get_guide(guide_id):
    guide = Guide.objects.get_or_404(id=guide_id)
    return guide
