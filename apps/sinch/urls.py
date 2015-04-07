from django.conf.urls import patterns, url
from apps.sinch import views
urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^ping/$', views.pingHandler, name='ping handler'),
        url(r'^login/$', views.ticketHandler, name='login handler'),
        url(r'^get-caller-info/$', views.getCallerInfo, name='caller user info'),
		)