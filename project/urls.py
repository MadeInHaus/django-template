
from django.conf import settings
from django.conf.urls import include, patterns, url
from django.contrib import admin
from django.views.generic import TemplateView

from tastypie.api import Api

from utils.s3proxy import S3ProxyView


admin.autodiscover()

v1_api = Api(api_name='v1')


urlpatterns = patterns('',
    (r'^grappelli/', include('grappelli.urls')),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^api/', include(v1_api.urls)),

)

# Used to show static assets out of the collected-static and user media out of the uploads directory.
# Note this must be turned of with SERVE_STATIC var in settings.py
# Used to show static assets out of the collected-static and user media out of the uploads directory.
# Note this must be turned of with SERVE_STATIC var in settings.py
if getattr(settings, 'SERVE_STATIC', False):
    urlpatterns += patterns('',
        url(r'^static/(?P<path>.*)$', S3ProxyView.as_view(), {'request_path': '/static/', 'bucket_path': '/static/'}),
        url(r'^uploads/(?P<path>.*)$', S3ProxyView.as_view(), {'request_path': '/uploads/', 'bucket_path': '/uploads/'}),
    )

# Serve from local folders
# if getattr(settings, 'SERVE_STATIC', False) and settings.SERVE_STATIC:
#     urlpatterns += patterns('',
#         url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT, 'show_indexes': False,}),
#         url(r'^uploads/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': False,}),
#     )
    
# api profile view for tastypie endpoints
if getattr(settings, 'DEBUG', False):
    urlpatterns += patterns('',
                            (r'^api_profile/v1/(?P<resource>.*)/$', 'utils.api_views.api_profile'),
                            )

if  getattr(settings, 'DEBUG', False) and getattr(settings, 'SHOW_TOOLBAR', False):
    import debug_toolbar
    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )



# Homepage catchall needs to go last.
urlpatterns += patterns('',
    # Homepage
    (r'^', TemplateView.as_view(template_name='index.html')),
)


