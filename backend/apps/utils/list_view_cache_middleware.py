'''
Created on Jul 12, 2013

@author: joshua
'''

from django.utils.encoding import smart_str
from django.core.cache import cache


import logging
log = logging.getLogger(__name__)



LIST_VIEW_CACHE_KEYS = {
                        'api_cache': set([
                            '/api/v1/projects/,',
                            '/api/v1/projects/,format:json',
                            '/api/v1/projects/,limit:0',
                            '/api/v1/projects/,limit:20',
                            '/api/v1/projects/,limit:20,offset:0',
                            ]),
                        }


def cache_key_str(request):
    query_list = ['{}:{}'.format(k, request.GET.get(k)) for k in request.GET]
    query_list.sort()
    query_str = ','.join(query_list)
    return '{},{}'.format(smart_str(request.path), smart_str(query_str))


def invalidate_list_cache(cache_name):
    if cache_name in LIST_VIEW_CACHE_KEYS:
        for key in LIST_VIEW_CACHE_KEYS[cache_name]:
            cache.set(key, None)

def check_key(key_name):
    for cache_name in LIST_VIEW_CACHE_KEYS:
        if key_name in LIST_VIEW_CACHE_KEYS[cache_name]:
            return True
    return False

def update(response):
    # do whatever is necessary to keep object up to date (like adjusting time objects)
    return response

class CacheGetListView(object):    
    def process_request(self, request):
#         log.debug(u'Method: {}  Path: {}'.format(request.method, request.path))
        if request.method not in ['GET', ]:
            return None
        
        key_str = cache_key_str(request)
        if check_key(key_str):
            response = cache.get(key_str, None)

            if response is not None:
#                 log.debug(u'cache found... updating: {}'.format(key_str))
                response = update(response)

            if response is None:
#                 log.debug(u'marking for save: {}'.format(key_str))
                request.cache_response = True

            return response

class CacheSetListView(object):
    def process_response(self, request, response):
        if request.method not in ['GET', ]:
            return response

        key_str = cache_key_str(request)
        if check_key(key_str):
            if hasattr(request, 'cache_response'):
#                 log.debug(u'setting cache for {} -- size: {}'.format(key_str, len(response.content)))
                cache.set(key_str, response)
            else:
                pass
#                 log.debug(u'skipping cache save: {}'.format(key_str))

        return response