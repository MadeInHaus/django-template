from django.contrib.staticfiles.storage import CachedFilesMixin
from django.core.files.base import ContentFile
from django.core.files.storage import Storage

from django.conf import settings

from storages.backends.s3boto import S3BotoStorage

from require.storage import OptimizedFilesMixin

import re

class OptimizedCachedS3BotoStorage(OptimizedFilesMixin, CachedFilesMixin, S3BotoStorage):
    pass

class OptimizedS3BotoStorage(OptimizedFilesMixin, S3BotoStorage):
    def url(self, name):
        name = self._normalize_name(self._clean_name(name))
        protocol = ( getattr(settings, 'AWS_S3_URL_PROTOCOL') 
                        if hasattr(settings, 'AWS_S3_URL_PROTOCOL') 
                    else
                        'https:' if self.secure_urls else 'http:'
                        )
        if self.custom_domain:
            return "%s//%s/%s" % (protocol, self.custom_domain, name)
        else:
            url = self.connection.generate_url(self.querystring_expire, method='GET', \
                    bucket=self.bucket.name, key=self._encode_name(name), query_auth=self.querystring_auth, \
                    force_http=not self.secure_urls)
            return re.sub('https?:',protocol,url)

class MediaRootS3BotoStorage(S3BotoStorage):
    def __init__(self, **kwargs):
        kwargs['location'] = 'uploads'
        super(MediaRootS3BotoStorage, self).__init__(**kwargs)

    def url(self, name):
        name = self._normalize_name(self._clean_name(name))
        protocol = ( getattr(settings, 'AWS_S3_URL_PROTOCOL') 
                        if hasattr(settings, 'AWS_S3_URL_PROTOCOL') 
                    else
                        'https:' if self.secure_urls else 'http:'
                        )
        if self.custom_domain:
            return "%s//%s/%s" % (protocol, self.custom_domain, name)
        else:
            url = self.connection.generate_url(self.querystring_expire, method='GET', \
                    bucket=self.bucket.name, key=self._encode_name(name), query_auth=self.querystring_auth, \
                    force_http=not self.secure_urls)
            return re.sub('https?:',protocol,url)


    def get_available_name(self, name):
        return Storage.get_available_name(self, name)
