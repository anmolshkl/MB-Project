from django.conf.urls import patterns, url
from apps.home import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^logout/$', views.user_logout, name='index'),
		url(r'^login/$', views.user_login, name='index'))