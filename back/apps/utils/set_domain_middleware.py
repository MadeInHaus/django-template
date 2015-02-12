from django.middleware.common import CommonMiddleware
from django.conf import settings

import logging
log = logging.getLogger(__name__)


class SetDomainMiddleware(CommonMiddleware):
    def process_request(self, request):
        if 'Amazon' not in request.META.get('HTTP_USER_AGENT', ''):
            log.debug('not a cloudfront request')
            return

        request_host = request.get_host()
        host = getattr(settings, 'SITE_DOMAIN', request_host)
        log.debug('setting domain {}  -->  {}'.format(request_host, host))
        ALLOWED_DOMAINS = getattr(settings, 'ALLOWED_DOMAINS', [host, ])
        if host != request_host and (request_host not in ALLOWED_DOMAINS):
            request.META['HTTP_HOST'] = host 
