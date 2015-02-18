from subprocess import call, os
from cStringIO import StringIO

from django.core.management.base import BaseCommand
from django.core import management
from django.conf import settings

from boto.s3.connection import S3Connection


def create_fixture(app_name, filename):
    buf = StringIO()
    management.call_command('dumpdata', app_name, stdout=buf, indent=4)
    buf.seek(0)
    with open(filename, 'w') as f:
        f.write(buf.read())

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
        fixtures_dir = os.path.abspath(os.path.join(BASE_DIR, 'backend', 'fixtures'))

        fixture_name = os.path.join(fixtures_dir, 'local_data.json')

        #TODO setup app name below
        create_fixture('CHANGE APP NAME', fixture_name)

        conn = S3Connection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
        bucket = conn.get_bucket(AWS_BUCKET_NAME)
        os.chdir(BASE_DIR)
        k = bucket.new_key('fixtures/local_data.json')
        k.set_contents_from_filename(fixture_name)
        k.set_acl('public-read')

