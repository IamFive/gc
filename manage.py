# -*- coding: utf-8 -*-
#
# Copyright (c) 2011-2013 Woo-cupid(iampurse#vip.qq.com)
#
from guildconnections.common import startup_app, init_db, clear_db
from flask_script import Manager
from flask.globals import current_app

manager = Manager(startup_app)

@manager.command
def initdb():
    """ Initialize database . """
    with current_app.app_context():
        init_db();

@manager.command
def cleardb():
    """Clear database ."""
    with current_app.app_context():
        clear_db();


if __name__ == '__main__':
    manager.run(default_command='runserver')
