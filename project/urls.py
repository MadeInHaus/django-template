import os

from django.conf import settings
from django.conf.urls.defaults import include, patterns, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView

admin.autodiscover()

urlpatterns = patterns('',
    (r'^grappelli/', include('grappelli.urls')),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
)

# Used to show static assets out of the collected-static and user media out of the uploads directory.
# Note this must be turned of with SERVE_STATIC var in settings.py
if getattr(settings, 'SERVE_STATIC', False) and settings.SERVE_STATIC:
    urlpatterns += patterns('',
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT, 'show_indexes': False,}),
        url(r'^uploads/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': False,}),
    )
    
# api profile view for tastypie endpoints
if getattr(settings, 'DEBUG', False):
    urlpatterns += patterns('',
                            (r'^api_profile/v1/(?P<resource>.*)/$', 'utils.api_views.api_profile'),
                            )

# Homepage catchall needs to go last.
urlpatterns += patterns('',
    # Homepage
    (r'^$', TemplateView.as_view(template_name='index.html')),
)


