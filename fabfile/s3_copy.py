from fabric.decorators import task, roles

from haus_vars import with_vars, APP_INFO, parse_vars
from fabric.api import run, execute
from fabric.context_managers import cd

from heroku import create_fixture_on_s3, grab_fixture_on_s3

import cStringIO



def copyBucket(srcBucketName, dstBucketName, aws_key, aws_secret, folder_name='uploads'):
    from boto.s3.connection import S3Connection
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


def copyBucketDifferentOwners(src_settings, dst_settings, folder_name='uploads'):
    from boto.s3.connection import S3Connection
    srcBucketName = src_settings['AWS_BUCKET_NAME']
    dstBucketName = dst_settings['AWS_BUCKET_NAME']
    src_conn = S3Connection(src_settings['AWS_ACCESS_KEY_ID'], src_settings['AWS_SECRET_ACCESS_KEY'])
    dst_conn = S3Connection(dst_settings['AWS_ACCESS_KEY_ID'], dst_settings['AWS_SECRET_ACCESS_KEY'])
    source = src_conn.get_bucket(srcBucketName);
    destination = dst_conn.get_bucket(dstBucketName);
    if folder_name:
        s3keys = source.list(folder_name)
    else:
        s3keys = source.list()

    for k in s3keys:
        print 'Copying ' + k.key + ' from ' + srcBucketName + ' to ' + dstBucketName
        f = cStringIO.StringIO()
        k.get_contents_to_file(f)
        nk = destination.new_key(k.key)
        f.seek(0)
        nk.set_contents_from_file(f, 
                                  policy='public-read', 
                                  headers={ 'Content-Type': k.content_type }
                                  )


@task
@roles('vagrant')
def update_uploads(src_env='staging', dst_env='dev', different_owners=False):
    """copies the uploads folder from src_env to dst_env s3 buckets, pass different_owners=True to copy between s3 buckets that belong to different accounts"""
    different_owners = str(different_owners).lowercase() == 'true'
    print "{}".format(APP_INFO)
    src_app_env = APP_INFO[src_env]['APP_ENV']
    dst_app_env = APP_INFO[dst_env]['APP_ENV']
    with(cd('/var/www')):
        src_settings = parse_vars(run("APP_ENV={} ./manage.py settings_vars AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY AWS_BUCKET_NAME".format(src_app_env)))
        dst_settings = parse_vars(run("APP_ENV={} ./manage.py settings_vars AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY AWS_BUCKET_NAME".format(dst_app_env)))
    src = src_settings['AWS_BUCKET_NAME']
    dst = dst_settings['AWS_BUCKET_NAME']
    folder = 'uploads'


    owners = {
              'dev': 1,
              'staging': 1,
              'production': 1,
              }

    if owners[src_env] != owners[dst_env]:
        copyBucketDifferentOwners(src_settings, dst_settings, folder)
    else:
        copyBucket(src, dst, src_settings['AWS_ACCESS_KEY_ID'], src_settings['AWS_SECRET_ACCESS_KEY'], folder)

@task
@roles('vagrant')
def update_fixture(src_env='staging', dst_env='dev', do_update_uploads=True, *args, **kwargs):
    """ updates fixture and downloads it for given src_env (staging by default) copies uploads directory from src_env to dst_env s3 buckets unless update_uploads=False"""
    if str(do_update_uploads).lower() == 'false':
        do_update_uploads = False
    execute(create_fixture_on_s3, env=src_env)
    execute(grab_fixture_on_s3, env=src_env)
    if update_uploads:
        execute(update_uploads, src_env=src_env, dst_env=dst_env)


