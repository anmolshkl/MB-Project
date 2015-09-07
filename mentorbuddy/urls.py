from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from django.views.generic import TemplateView

admin.autodiscover()

urlpatterns = patterns('',
                       url('', include('social.apps.django_app.urls', namespace='social')),
                       url(r'^$', include('apps.user.urls')),
                       url(r'^user/', include('apps.user.urls')),
                       url(r'^mentor/', include('apps.mentor.urls')),
                       url(r'^mentee/', include('apps.mentee.urls')),
                       url(r'^live/', include('apps.sinch.urls')),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^search/', include('apps.user.urls')),
                       url(r'^about/$', TemplateView.as_view(template_name='about.html'), name='about')
                       )

# UNDERNEATH your urlpatterns definition, add the following two lines:
if settings.DEBUG:
    urlpatterns += patterns(
        'django.views.static',
        (r'media/(?P<path>.*)',
         'serve',
         {'document_root': settings.MEDIA_ROOT}), )
