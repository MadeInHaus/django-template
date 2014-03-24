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

class S3ProxyView(View):
    def get(self, request, bucket_path):
        aws_key = getattr(settings, 'AWS_ACCESS_KEY_ID', None)
        aws_secret = getattr(settings, 'AWS_SECRET_ACCESS_KEY', None)
        aws_bucket = getattr(settings, 'AWS_BUCKET_NAME', None)
        if None in [aws_key, aws_secret, aws_bucket]:
            return HttpResponseServerError('aws configuration error')

        conn = S3Connection(aws_key, aws_secret)
        bucket = conn.get_bucket(aws_bucket)
        
        file_ = bucket.get_key(bucket_path)

        if not file_:
            return HttpResponseNotFound()

        return HttpResponse(file_.open(), content_type=file_.content_type)
        