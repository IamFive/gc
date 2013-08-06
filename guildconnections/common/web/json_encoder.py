# -*- coding: utf-8 -*-
#
# @author: Five
# Created on 2013-4-19
#

import datetime
import json
from bson.objectid import ObjectId
from mongoengine.document import Document, DynamicDocument
from mongoengine.queryset import QuerySet
from bson.dbref import DBRef

class MongoExtEncoder(json.JSONEncoder):
    """json encoder for mongoengine model
    """

    def __init__(self, only=None, exclude=None, **kwargs):
        """Reminds:
            1. only and exclude should not appear in the same time.
            2. only and exclude are only effect on mongoengine-document objects
            3. key use a seperate for . to support subobject

            :param only: a tuple contains the keys to be dumps
            :param exclude: a tuple excludes the keys not to be dumps


            ie: only = ('name', 'location.city'), the encoder should only dump this two key.
        """

        json.JSONEncoder.__init__(self, **kwargs);

        self.only = self.build_filter(only) if only else None
        default_exclude = ['_types', '_cls']
        if exclude:
            default_exclude.extend(exclude)
        self.exclude = self.build_filter(default_exclude)

    def build_filter(self, keys):

        if not isinstance(keys, (list, tuple)):
            keys = (keys,)

        result = {}
        for key in keys:
            split = key.split('.')
            if len(split) > 1:
                result[split[0]] = self.build_filter('.'.join(split[1:]))
            else:
                result[key] = None
        return result


    def filter_by_only(self, source, only):
        keys = source.keys()
        for key in keys:
            if not key in only:
                del source[key]
            elif only[key]:
                source[key] = self.filter_by_only(source.pop(key), only[key])
        return source

    def filter_by_exclude(self, source, exclude):
        keys = source.keys()
        for key in keys:
            if key in exclude:
                if exclude[key]:
                    source[key] = self.filter_by_exclude(source.pop(key), exclude[key])
                else:
                    del source[key]
        return source

    def default(self, obj):
        if isinstance(obj, QuerySet):
            iterable = iter(obj)
            return list(iterable)
        elif isinstance(obj, (Document, DynamicDocument)):
            as_dict = obj.to_mongo()
            if self.only:
                return self.filter_by_only(as_dict, self.only)
            elif self.exclude:
                return self.filter_by_exclude(as_dict, self.exclude)
            return as_dict
        elif isinstance(obj, ObjectId):
            return str(obj)
        elif isinstance(obj, datetime.datetime):
            if obj.utcoffset() is not None:
                obj = obj - obj.utcoffset()
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, DBRef):
            return obj.id


        raise TypeError("%r is not JSON serializable, please add path in %s"
                        % (type(obj), self.__class__.__name__))


