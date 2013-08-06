# -*- coding: utf-8 -*-
#
# Copyright (c) 2011-2013 Woo-cupid(iampurse#vip.qq.com)
#
from guildconnections.common.exceptions import FriendlyException
from werkzeug.datastructures import MultiDict
import copy
import urllib
import urlparse


def build_url(url, params):
    urlparts = list(urlparse.urlparse(url))
    query = dict(urlparse.parse_qsl(urlparts[4]))
    query.update(params)
    urlparts[4] = urllib.urlencode(query)
    return urlparse.urlunparse(urlparts)


#===============================================================================
# ParseResult(
#    scheme='http',
#    netloc='localhost',
#    path='/authorize/index',
#    params='',
#    query='next=%2Fauthorize%2Fprivate',
#    fragment=''
# )
#===============================================================================
def get_url_part(url, part):
    parsed = urlparse.urlparse(url)
    return getattr(parsed, part);

def get_url_query_as_dict(url):
    query_string = get_url_part(url, 'query')
    return dict(urlparse.parse_qsl(query_string));

def json_2_formdata(source, prefix=None, seperator='-'):

    def list_2_formdata(source, prefix=None, seperator='-'):
        """
            handle list item
        """
        dist = {}
        prefix = '' if not prefix else prefix + seperator
        for idx, item in enumerate(source):
            prefix_with_idx = prefix + str(idx)
            if isinstance(item, list):
                dist.update(list_2_formdata(item, prefix_with_idx, seperator))
            elif isinstance(item, dict):
                dist.update(dict_2_formdata(item, prefix_with_idx, seperator))
            else:
                dist[prefix_with_idx] = item
        return dist

    def dict_2_formdata(source, prefix=None, seperator='-'):
        dist = {}
        prefix = '' if not prefix else prefix + seperator
        for key, value in source.items():
            if isinstance(value, dict):
                sub_dict = source.pop(key)
                dist.update(json_2_formdata(sub_dict, prefix + key, seperator))
            elif isinstance(value, list):
                item_list = source.pop(key)
                dist.update(list_2_formdata(item_list, prefix + key, seperator))
            else:
                dist[prefix + key] = value
        return dist

    # copy source but not modify it directly
    if isinstance(source, dict):
        source_copy = source.copy()
        return dict_2_formdata(source_copy, prefix, seperator)
    elif isinstance(source, list):
        source_copy = copy.deepcopy(source)
        return list_2_formdata(source_copy, prefix, seperator)

def get_formdata(request):
    if request.json:
        formdata = MultiDict(json_2_formdata(request.json))
        return formdata

    return request.values

def str2bool(sv):

    lower_value = sv.lower()
    if lower_value in ("yes", "true", "t", "1"):
        return True
    elif sv.lower() in ("no", "false", "f", "0"):
        return False

    raise FriendlyException(104, 'value %s cant be convert to bool' % lower_value)


def mkdirs(path, is_folder=False):
    import os.path
    if not is_folder:
        path = os.path.dirname(path)
    if not os.path.exists(os.path.abspath(path)):
        os.makedirs(os.path.abspath(path))

