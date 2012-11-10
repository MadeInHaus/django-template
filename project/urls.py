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
    # Homepage
    #(r'^$', TemplateView.as_view(template_name='home.html')),
)

# Static files only get served by django in DEBUG mode
if settings.DEBUG:

    # Add local directory to root
    local_path = os.path.join(settings.DEV_STATIC_ROOT, 'local')
    if os.path.exists(local_path):
        for fname in os.listdir(local_path):
            parts.append(url(r'^(?P<path>%s)' % fname,
                'django.views.static.serve', {'document_root': local_path}))

    urlpatterns += staticfiles_urlpatterns()
