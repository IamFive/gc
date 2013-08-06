# -*- coding: utf-8 -*-
#
# @author: Five
# Created on 2013-4-28
#
import os
from flask.config import Config
from guildconnections.constants import BASE, ROOT

class Resource():

    def __init__(self, path, covered=None):
        self._path = path
        self._covered = covered

    @property
    def path(self):
        return self._path

    @property
    def covered(self):
        return self._covered

    def as_list(self):
        result = []
        if self._covered:
            result.append(self._covered)
        result.append(self._path)
        return result


class ResourceLoader():
    """ common resource loader """

    ENV_VAR_NAME = 'GC_RESOURCE_FOLDER'

    COVERED_FOLDER = 'default'
    DFT_BASE_FOLDER = './resources/dev'

    def __init__(self):
        self.base_folder = self.init_base_folder()
        self.covered_folder = self.init_covered_folder()

    def _add_sep(self, path):
        return path if path.endswith(os.pathsep) else path + os.path.sep

    @property
    def _dft_base_folder(self):
        """ point to the resources/dev under project root """
        return os.path.abspath(os.path.join(BASE, self.DFT_BASE_FOLDER))

    def init_base_folder(self):
        folder = os.environ.get(self.ENV_VAR_NAME, None)
#        info('resource folder path from env is: {}'.format(folder))
#        print 'resource folder path from env is: {}'.format(folder)
        folder = folder if folder else self._dft_base_folder
        return folder

    def init_covered_folder(self):
        base = self._add_sep(self.base_folder)
        path = os.path.join(base, '..', self.COVERED_FOLDER)
        return os.path.abspath(path)


    @classmethod
    def get(cls):
        if not hasattr(cls, '_rl'):
            cls._rl = ResourceLoader()
        return cls._rl

    @classmethod
    def reload(cls):
        if hasattr(cls, '_rl'):
            del cls._rl
        return cls.get()


    def get_resoure(self, path, validate=False, with_cover=False):
        """
        get absolute resource path

        Param:
            path - the relatived path to the resource folder
            validate - whether validate the return path is a valid path(Not implement)
            with_cover - whether load the default file in default folder

        Return:
            a absolute path

        """
        resource_path = os.path.abspath(os.path.join(self.base_folder, path))
        if self.covered_folder:
            covered_path = os.path.abspath(os.path.join(self.covered_folder, path))
            if os.path.exists(covered_path):
                return Resource(resource_path, covered_path)
        return Resource(resource_path)

    @property
    def configs(self):
        if not hasattr(self, '_configs'):
            configs = Config(ROOT)
            resoure = ResourceLoader.get().get_resoure('settings.py')
            config_files = resoure.as_list()
            if config_files:
                for path in config_files:
                    configs.from_pyfile(path)
            else:
                raise Exception('need a configuration file to start app')

            self._configs = configs
        return self._configs
