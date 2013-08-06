# -*- coding: utf-8 -*-
#
# @author: Five
# Created on 2013-6-1
#
from flaskext.uploads import UploadSet, IMAGES

Avatars = UploadSet('avatar', IMAGES)
Logos = UploadSet('logo', IMAGES)

upload_list = (Avatars, Logos)
