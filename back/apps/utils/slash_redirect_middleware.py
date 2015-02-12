from django.middleware.common import CommonMiddleware
from django.conf import settings
from django.core import urlresolvers
from django.utils.http import urlquote
from django.utils import six
from django import http


class SlashRedirectMiddleware(CommonMiddleware):
    def append_slash(self, request, host):
        old_url = [host, request.path]
        new_url = old_url[:]

        if not old_url[1].endswith('/'):
            urlconf = getattr(request, 'urlconf', None)
            if (not urlresolvers.is_valid_path(request.path_info, urlconf) and
                    urlresolvers.is_valid_path("%s/" % request.path_info, urlconf)):
                new_url[1] = new_url[1] + '/'
                if settings.DEBUG and request.method == 'POST':
                    raise RuntimeError((""
                    "You called this URL via POST, but the URL doesn't end "
                    "in a slash and you have APPEND_SLASH set. Django can't "
                    "redirect to the slash URL while maintaining POST data. "
                    "Change your form to point to %s%s (note the trailing "
                    "slash), or set APPEND_SLASH=False in your Django "
                    "settings.") % (new_url[0], new_url[1]))

        if new_url == old_url:
            # No redirects required.
            return
        

        if new_url[0]:
            newurl = "%s://%s%s" % (
                request.is_secure() and 'https' or 'http',
                new_url[0], urlquote(new_url[1]))
        else:
            newurl = urlquote(new_url[1])
        if request.META.get('QUERY_STRING', ''):
            if six.PY3:
                newurl += '?' + request.META['QUERY_STRING']
            else:
                # `query_string` is a bytestring. Appending it to the unicode
                # string `newurl` will fail if it isn't ASCII-only. This isn't
                # allowed; only broken software generates such query strings.
                # Better drop the invalid query string than crash (#15152).
                try:
                    newurl += '?' + request.META['QUERY_STRING'].decode()
                except UnicodeDecodeError:
                    pass
        return http.HttpResponsePermanentRedirect(newurl)

        
    def process_request(self, request):
        host = getattr(settings, 'SITE_DOMAIN', request.get_host())
        return self.append_slash(request, host)