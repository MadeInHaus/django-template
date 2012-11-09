import os
import sys
from django.conf import settings

# Prevent interactive question about wanting a superuser created
# since the admin user is already created through the initial data
# (taken from http://stackoverflow.com/questions/1466827/)
from django.db.models import signals
from django.contrib.auth.management import create_superuser
from django.contrib.auth import models as auth_app
signals.post_syncdb.disconnect(create_superuser, sender=auth_app,
    dispatch_uid = "django.contrib.auth.management.create_superuser")
