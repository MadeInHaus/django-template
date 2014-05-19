from subprocess import call, os

from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = "Loads fixture images from S3 bucket,  optional bucket name argument"

    def handle(self, *args, **options):
        if len(args)>0:
            AWS_BUCKET_NAME = args[0]
        else:
            AWS_BUCKET_NAME = settings.AWS_BUCKET_NAME

        self.stdout.write('Using bucket: {}'.format(AWS_BUCKET_NAME))

        BASE_DIR = settings.BASE_DIR

        uploads_dir = os.path.abspath(os.path.join(BASE_DIR, 'uploads'))
        os.chdir(BASE_DIR)
        call('mkdir -p {}'.format(uploads_dir), shell=True)
        os.chdir(uploads_dir)
        try:
            call('rm -rf ./*', shell=True)
        except Exception as e:
            print e  # probably an empty directory
        call(
             'curl -sLO http://{}.s3.amazonaws.com/fixtures/assets.tar.bz2'.format(AWS_BUCKET_NAME),
             shell=True
             )
        call('tar xjvf assets.tar.bz2', shell=True)
        call('rm assets.tar.bz2', shell=True)
