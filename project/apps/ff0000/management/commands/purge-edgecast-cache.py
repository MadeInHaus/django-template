from optparse import make_option
import httplib
import json
import urllib

from django.conf import settings
from django.core.management.base import CommandError
from django.core.management.base import BaseCommand
from django.db import connection

API_DOMAIN = "api.edgecast.com"
API_PATH = "/v2/mcc/customers/%s/edge/purge"

SETTINGS_URL = 'CDN_URL'
SETTINGS_CUSTOMER = 'CDN_CUSTOMER_ID'
SETTINGS_TYPE = 'CDN_TYPE'
SETTINGS_ACCESS = 'CDN_ACCESS_KEY'

error_message = """You must specify the required options either in your settings file or as an option to this command.

Required:
Full CDN URL: use --cdn= or %s in your settings file.
Customer id: use --customer= or %s in your settings file.
Access Key: use --key= or %s in your settings file.

Optional
CDN type: use --type= or %s in your settings file. Defaults to 8, small http.
""" % (SETTINGS_URL, SETTINGS_CUSTOMER, SETTINGS_TYPE, SETTINGS_ACCESS )

class Command(BaseCommand):
    help = "Purge a Edgecast CDN Cache"

    option_list = BaseCommand.option_list + (
        make_option('--customer', action="store", type="string", dest="customer"),
        make_option('--cdn', action="store", type="string", dest="cdn"),
        make_option('--type', action="store", type="string", dest="type"),
        make_option('--key', action="store", type="string", dest="key"),
        )

    def clear_cache(self, cdn_url, customer_id, access_key, cdn_type):
        url = API_PATH % customer_id

        if not cdn_url.endswith('/'):
            cdn_url = cdn_url + '/'

        data = json.dumps({
            "MediaPath": cdn_url + '*',
            "MediaType": cdn_type
        })

        headers = {
            "Authorization" : "TOK:%s" % access_key,
            "Accept" : "application/json",
            "Content-Type" : "application/json"
        }

        conn = httplib.HTTPSConnection(API_DOMAIN)
        conn.request("PUT", url, data, headers)

        response = conn.getresponse()
        data = response.read()
        if response.status != 200:
            e = ["Got Unexpected response: %s" % response.status, data]
            raise CommandError('\n'.join(e))
        else:
            print "Cache flush accepted."

    def handle(self, *args, **options):
        cdn_url = getattr(settings, SETTINGS_URL, options.get('cdn'))
        customer_id = getattr(settings, SETTINGS_CUSTOMER, options.get('customer'))
        cdn_type = getattr(settings, SETTINGS_TYPE, options.get('type'))
        access_key = getattr(settings, SETTINGS_ACCESS, options.get('key', 3))

        if not cdn_url or not customer_id or not access_key:
            raise CommandError(error_message)

        if not cdn_type:
            cdn_type = 8

        self.clear_cache(cdn_url, customer_id, access_key, cdn_type)
