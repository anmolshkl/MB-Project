from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^accounts/', include('allauth.urls')),
    url(r'^$', include('apps.user.urls')),
    url(r'^user/', include('apps.user.urls')),
    url(r'^mentor/', include('apps.mentor.urls')),
    url(r'^mentee/', include('apps.mentee.urls')),
    url(r'^admin/', include(admin.site.urls)),

)

# UNDERNEATH your urlpatterns definition, add the following two lines:
if settings.DEBUG:
    urlpatterns += patterns(
        'django.views.static',
        (r'media/(?P<path>.*)',
        'serve',
        {'document_root': settings.MEDIA_ROOT}), )
