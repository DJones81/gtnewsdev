from django.conf.urls import patterns, include, url
from gtnewsdev.settings import STATIC_ROOT

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^geonewsapi/', include('gtnewsdev.geonewsapi.urls')),
#    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('',
    url(r'^static/(.*)$', 'django.views.static.serve', {'document_root': STATIC_ROOT, 'show_indexes' : True}),
)