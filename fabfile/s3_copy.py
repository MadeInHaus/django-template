from boto.s3.connection import S3Connection
from fabric.decorators import task, roles

from haus_vars import with_vars, APP_INFO, parse_vars
from fabric.operations import run
from fabric.context_managers import cd


def copyBucket(srcBucketName, dstBucketName, aws_key, aws_secret, folder_name='uploads'):
    conn = S3Connection(aws_key, aws_secret)
    source = conn.get_bucket(srcBucketName);
    destination = conn.get_bucket(dstBucketName);
    if folder_name:
        s3keys = source.list(folder_name)
    else:
        s3keys = source.list()

    for k in s3keys:
        print 'Copying ' + k.key + ' from ' + srcBucketName + ' to ' + dstBucketName
        destination.copy_key(k.key, srcBucketName, k.key, preserve_acl=True)


@task
@roles('vagrant')
def update_dev_uploads(src_env='staging', dst_env='dev', *args, **kwargs):
    """copies the uploads folder from src_env to dst_env s3 buckets"""
    print "args: {} kwargs: {}".format(args, kwargs)
    print "{}".format(APP_INFO)
    src_app_env = APP_INFO[src_env]['APP_ENV']
    dst_app_env = APP_INFO[dst_env]['APP_ENV']
    with(cd('/var/www')):
        src_settings = parse_vars(run("APP_ENV={} ./manage.py settings_vars AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY AWS_BUCKET_NAME".format(src_app_env)))
        dst_settings = parse_vars(run("APP_ENV={} ./manage.py settings_vars AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY AWS_BUCKET_NAME".format(dst_app_env)))
    src = src_settings['AWS_BUCKET_NAME']
    dst = dst_settings['AWS_BUCKET_NAME']
    folder = 'uploads'
    copyBucket(src, dst, src_settings['AWS_ACCESS_KEY_ID'], src_settings['AWS_SECRET_ACCESS_KEY'], folder)
    