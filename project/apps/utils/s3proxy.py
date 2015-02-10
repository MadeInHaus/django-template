'''
Proxy view for serving files from s3 bucket from Django.

Created on Feb 18, 2014

@author: joshua
'''

from django.views.generic.base import View

from boto.s3.connection import S3Connection

from django.conf import settings
from django.http.response import HttpResponseServerError, HttpResponse,\
    HttpResponseNotFound

import gzip
import StringIO

class S3ProxyView(View):
    path = None
    bucket_path=u'/'
    request_path=u'/static/'
    def get(self, request, path = None, bucket_path=u'/', request_path=u'/static/'):
        print "path:{} bucket_path:{} request_path:{}".format(path.encode('utf8'), bucket_path, request_path)
        aws_key = getattr(settings, 'AWS_ACCESS_KEY_ID', None)
        aws_secret = getattr(settings, 'AWS_SECRET_ACCESS_KEY', None)
        aws_bucket = getattr(settings, 'AWS_BUCKET_NAME', None)
        if None in [aws_key, aws_secret, aws_bucket]:
            return HttpResponseServerError('aws configuration error')

        if path is None:
            path = request.path
            if not path.startswith(request_path):
                return HttpResponseServerError('path error: {} does not start with {}'.format(path, request_path))
            path = path[len(request_path):]
        path = bucket_path + path
        
        conn = S3Connection(aws_key, aws_secret)
        bucket = conn.get_bucket(aws_bucket)

        print "s3proxy requesting path: {}".format(path.encode('utf8'))

        file_ = bucket.get_key(path)

        if not file_:
            return HttpResponseNotFound()

        content = StringIO.StringIO()
        file_.get_file(content)
        content.seek(0)
        try:
            gzf = gzip.GzipFile(fileobj=content)
            content = gzf.read()
        except:
            content.seek(0)
        return HttpResponse(content, content_type=file_.content_type)
        