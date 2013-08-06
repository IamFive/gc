# -*- coding: utf-8 -*-
#
# @author: Five
# Created on 2013-4-2
#

import random
import json
from datetime import datetime
from guildconnections.common.choices import Status
from flask.globals import request, current_app
# from mongoengine import Document, DynamicDocument
# from flask.ext.mongoengine import Document, DynamicDocument
from flask_mongoengine import Document, DynamicDocument, BaseQuerySet, Pagination
from mongoengine.fields import DateTimeField, IntField, StringField
from mongoengine.queryset import QuerySet
from guildconnections.common.exceptions import FriendlyException
from guildconnections.common import error_code
from flask_login import current_user
from mongoengine.document import EmbeddedDocument
from mongoengine.errors import DoesNotExist, MultipleObjectsReturned, \
    ValidationError

class PaginateHelper():

    @staticmethod
    def owner_mixin_filter():
        form_data = request.values or request.json or {}
        where = json.loads(form_data.get('where', '{}'))
        where['created_by'] = current_user.id
        return where


class BaseQuerySetMixin(BaseQuerySet):

    def get_or_404(self, *args, **kwargs):
        try:
            return self.get(*args, **kwargs)
        except (MultipleObjectsReturned, DoesNotExist, ValidationError), e:
            # current_app.logger.exception(e)
            if current_app.debug:
                raise FriendlyException(404, e.message)
            raise FriendlyException(404, 'Resource is not exists.')

    def paginate(self, where=None, limit=None, page=None, sort=None, only=(), exclude=()):

        form_data = request.values or request.json or {}
        where = where if where else json.loads(form_data.get('where', '{}'))
        limit = int(limit if limit else form_data.get('limit', 20))
        page = int(page if page else form_data.get('page', 1))
        sort = sort if sort else form_data.get('sort', None)

        if limit <= 0 or limit > 200 or page <= 0:
            raise FriendlyException.from_error_code(error_code.INVALID_PAGINATE)

        querySet = self.filter(**where)
        if len(only):
            querySet = querySet.only(*only)

        if len(exclude):
            querySet = querySet.exclude(*exclude)

        if sort:
            querySet = querySet.order_by(sort)

        paginate = PaginationMixin(querySet, page, limit)
        return paginate.to_dict()

class PaginationMixin(Pagination):

    def __init__(self, iterable, page, limit):

        self.iterable = iterable
        self.total = len(iterable)
        self.page = page
        self.limit = limit

        start_index = (page - 1) * limit
        end_index = page * limit

        if start_index <= self.total:
            self.items = iterable[start_index:end_index]
            if isinstance(self.items, QuerySet):
                self.items = self.items.select_related()

        if not hasattr(self, 'items'):
            self.items = []

    def to_dict(self):
        return {
            'page' : self.page,
            'limit' : self.limit,
            'total' : self.total,
            'data' : self.items
        }

class BaseModel(Document):

    created = DateTimeField(default=datetime.now)
    modified = DateTimeField(default=datetime.now)

    created_by = StringField()
    modified_by = StringField()

    status = IntField(default=Status.VALID)

    meta = {'abstract': True,
            'queryset_class': BaseQuerySetMixin}

    #===============================================================================
    # we can add operate log here too.
    #===============================================================================
    def save(self, *args, **kwargs):
        try:
            if not self.created_by:
                self.created_by = current_user.get_id()
            self.modified_by = current_user.get_id()
        except:
            pass

        self.modified = datetime.now()
        Document.save(self, **kwargs)

    def update(self, *args, **kwargs):
        try:
            if not self.created_by:
                self.created_by = current_user.get_id()
            self.modified_by = current_user.get_id()
        except:
            pass

        self.modified = datetime.now()
        return Document.update(self, *args, **kwargs)

    def delete(self, *args, **kwargs):
        # we can custom the delete
        # example: set the status to 0 instead of physical delete
        return Document.delete(self, *args, **kwargs)


class BaseDynamicModel(DynamicDocument):

    created = DateTimeField(default=datetime.now)
    modified = DateTimeField(default=datetime.now)

    created_by = StringField()
    modified_by = StringField()

    status = IntField(default=Status.VALID)

    meta = {'abstract': True,
            'queryset_class': BaseQuerySetMixin}


    def save(self, *args, **kwargs):
        if not self.created_by:
            self.created_by = current_user.get_id()
        self.modified = datetime.now()
        self.modified_by = current_user.get_id()
        Document.save(self, **kwargs)

    def update(self, *args, **kwargs):
        self.modified = datetime.now()
        self.modified_by = current_user.get_id()
        return Document.update(self, *args, **kwargs)



class IndexableString(EmbeddedDocument):
    """
        make StringField indexable
    """

    index = StringField()
    value = StringField()

    meta = {
        'allow_inheritance' : False
    }


    def __init__(self, index='', value=''):
        super(EmbeddedDocument, self).__init__()
        EmbeddedDocument.__init__(self)
        self.index = index
        self.value = value

    def __unicode__(self):
        return '''index %s, value %s.''' % (self.index, self.value)


    @staticmethod
    def build_from_list(string_list):

        list_len = len(string_list)
        index_list = range(1, list_len + 1)

        result_list = []
        for value in string_list:
            index = random.choice(index_list)
            index_list.remove(index)
            result_list.append(IndexableString(str(index), str(value)))

        return result_list



