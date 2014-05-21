'''
Created on Sep 26, 2013

@author: joshua
'''

from django.utils.cache import patch_response_headers
from django.conf import settings

import re

import logging
log = logging.getLogger(__name__)

class CachetimeLookup(object):
    def __init__(self, default=3601, patterns = None):
        self.default = default
        self.patterns = list((re.compile(pattern),timeout) for (pattern,timeout) in patterns or ())
        

    def get_cache_time(self, path):
        log.debug('matching path: {} '.format(path))
        for (pattern,timeout) in self.patterns:
            log.debug('pattern: {}'.format(pattern.pattern))
            if pattern.match(path):
                log.debug('path: {0} matched: {1} timeout: {2} '.format(path, pattern.pattern, timeout))
                return timeout
        log.debug('no match found')
        return self.default

APP_DEFAULT_CACHE = getattr(settings, 'APP_DEFAULT_CACHE', 3600)
APP_DEFAULT_SHORT_CACHE = getattr(settings, 'APP_DEFAULT_SHORT_CACHE', 600)

cache_lookup = CachetimeLookup(
                             default=getattr(settings, 'CACHE_MIDDLEWARE_SECONDS', 3601),
                             patterns = (
                                         (u'/banner/', APP_DEFAULT_SHORT_CACHE),
                                         (u'/company/(press|news)/.*', APP_DEFAULT_SHORT_CACHE),
                                         (u'/admin/.*', 0),
                                         (u'/', APP_DEFAULT_CACHE),
                                         )
                             )

def get_headers(request):
    regex = re.compile('^HTTP_')
    d = dict((regex.sub('', header), value) for (header, value) 
           in request.META.items() if header.startswith('HTTP_'))
    return d

class CacheHeadersMiddleware(object):
    """ overrides all Cache-Control settings on responses and injects headers from django.utils.cach.patch_response_headers """

    def process_response(self, request, response):
        log.debug("host: {}".format(request.get_host()))
        log.debug("headers: {}".format(get_headers(request)))
        if request.method in ['GET', 'HEAD']:
            path = request.path
            max_age = cache_lookup.get_cache_time(path)

            log.debug( 'CACHING: {} max_age: {}'.format(path, max_age) )

            # dump current Cache-Control headers
            del response['Cache-Control']
            # inject headers
            patch_response_headers(response, cache_timeout=max_age)

        return response
