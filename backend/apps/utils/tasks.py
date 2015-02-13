from __future__ import absolute_import

from celery import shared_task
from celery.decorators import periodic_task

from datetime import timedelta

import requests

import logging
log = logging.getLogger(__name__)

@shared_task
def test(msg):
    result = u"Got: {}".format(msg)
    log.debug(result)
    return result
