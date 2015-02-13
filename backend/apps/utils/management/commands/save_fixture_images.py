from subprocess import call, os

from django.core.management.base import BaseCommand
from django.conf import settings

from boto.s3.connection import S3Connection


class Command(BaseCommand):
    help = "Loads fixture images from S3 bucket"

    def handle(self, *args, **options):
        if len(args)>0:
            AWS_BUCKET_NAME = args[0]
        else:
            AWS_BUCKET_NAME = settings.AWS_BUCKET_NAME

        AWS_ACCESS_KEY_ID = settings.AWS_ACCESS_KEY_ID
        AWS_SECRET_ACCESS_KEY = settings.AWS_SECRET_ACCESS_KEY

        self.stdout.write('Using bucket: {}'.format(AWS_BUCKET_NAME))

        BASE_DIR = settings.BASE_DIR
        uploads_dir = os.path.abspath(os.path.join(BASE_DIR, 'uploads'))

        os.chdir(uploads_dir)
        call('tar cjvf assets.tar.bz2 *', shell=True)
        call('mv assets.tar.bz2 ..', shell=True)
        conn = S3Connection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
        bucket = conn.get_bucket(AWS_BUCKET_NAME)
        os.chdir(BASE_DIR)
        k = bucket.new_key('fixtures/assets.tar.bz2')
        k.set_contents_from_filename('assets.tar.bz2')
        k.set_acl('public-read')

