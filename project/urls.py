import os

from django.conf import settings
from django.conf.urls.defaults import include, patterns, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView

admin.autodiscover()
print(settings.STATIC_ROOT)

urlpatterns = patterns('',
    (r'^grappelli/', include('grappelli.urls')),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),

    # Homepage
    (r'^$', TemplateView.as_view(template_name='index.html')),
)

#used to show static assets out of the collected-static
if getattr(settings, 'REQUIRE_DEBUG', False) and settings.REQUIRE_DEBUG:
    urlpatterns += patterns('',
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT, 'show_indexes': False,}),
    )
