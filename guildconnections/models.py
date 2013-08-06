# -*- coding: utf-8 -*-
#
# @author: Five
# Created on 2013-5-14
#
from flask_mongoengine.wtf.orm import model_form
from guildconnections.choices import Gender, Boolean
from guildconnections.common.orm import BaseModel
from guildconnections.constants import DEFAULT_FORM_EXCLUDE
from mongoengine.document import EmbeddedDocument
from mongoengine.fields import (StringField, DateTimeField, IntField,
    ReferenceField, ListField, EmbeddedDocumentField, EmailField, URLField)
import datetime

class GuideType(BaseModel):
    """ use mongo DB to store the guild type,
        then we can add it dynamic without changing code"""
    name = StringField()
    meta = {
        'allow_inheritance' : False
    }

    def __unicode__(self):
        return '<GuideType::{}>'.format(self.guide_type)


class Game(BaseModel):
    """ game mongo model """
    name = StringField(max_length=128)
    description = StringField(max_length=512)

    meta = {
        'allow_inheritance' : False
    }

    def __unicode__(self):
        return '<Game::{}>'.format(self.name)


class Recruitment(EmbeddedDocument):

    find_guide = StringField(max_length=3, choices=Boolean.choices)
    find_for_game = ReferenceField(Game, dbref=False)
    find_for_type = ReferenceField(GuideType, dbref=False)
#    find_for_game = ReferenceField(Game, default=Game)
#    find_for_type = ReferenceField(GuideType, default=GuideType)

    current_realm = StringField()
    transfer_realm = StringField(max_length=3, choices=Boolean.choices)
    preffered_role = StringField()

    meta = {
        'allow_inheritance' : False
    }


class Gamer(EmbeddedDocument):

    avatar = StringField(max_length=512)

    # in the psd-gamer setup page, it's age.?
    dob = DateTimeField()
    gender = StringField(max_length=1, choices=Gender.choices,
                         default=Gender.U)

    bio = StringField(max_length=512)

    # maybe this is a choice too
    avg_play_time = IntField()
    timezone = IntField()

    # or we use string field instead?
    games = ListField(ReferenceField(Game, dbref=False))

    forum_signature = StringField(max_length=512)

    # Recruitment properties
    # TODO, dont know whether it's required.
    find_guide = StringField(max_length=3,
                             choices=Boolean.choices,
                             default=Boolean.NO)
    find_for_game = ReferenceField(Game, dbref=False)
    find_for_type = ReferenceField(GuideType, dbref=False)

    current_realm = StringField()
    transfer_realm = StringField(max_length=3,
                                 choices=Boolean.choices,
                                 default=Boolean.NO)
    preffered_role = StringField()


    meta = {
        'allow_inheritance' : False
    }

class User(BaseModel):
    """ user mongo model """

    email = EmailField(required=True, unique=True)

    # where is the user account and password?
    # we use this name field for user nick now.
    # if we need a new field for gamer profile setup, add it later
    name = StringField(max_length=128, required=True)
    password = StringField(max_length=16, required=True)

    # used when validate email
    verify_code = StringField(max_length=6)

    gamer = EmbeddedDocumentField(Gamer, default=Gamer)

    last_login_on = DateTimeField(default=datetime.datetime.now)

    meta = {
        'allow_inheritance' : False
    }



class Guide(BaseModel):
    """ guide mongo model """

    name = StringField(required=True)
    logo = StringField()
    url = URLField()
    description = StringField()
    founded_on = DateTimeField()

    min_age_required = IntField()
    gender_required = StringField(max_length=1, choices=Gender.choices,
                                  default=Gender.U)

    play_time_required = StringField()
    play_type = StringField()

    weekly_play_time = IntField()
    timezone = IntField()

    prime_time_from = IntField()
    prime_time_to = IntField()

    previous_games = StringField()
    voice = StringField(max_length=3, choices=Boolean.choices,
                        default=Boolean.NO)

    meta = {
        'allow_inheritance' : False
    }


user_form_exclude = list(DEFAULT_FORM_EXCLUDE)
user_form_exclude.extend(('last_login_on', 'verify_code'))
guid_form_exclude = DEFAULT_FORM_EXCLUDE + ('logo',)

UserForm = model_form(User, exclude=user_form_exclude)
GamerForm = model_form(Gamer, exclude=DEFAULT_FORM_EXCLUDE)
GuideForm = model_form(Guide, exclude=guid_form_exclude)
