from django.conf.urls import patterns, url
from apps.user import views
urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^logout/$', views.user_logout, name='logout'),
		url(r'^login/$', views.user_login, name='login'),
		url(r'^register/$', views.register, name='register'),
		url(r'^select/$', views.select, name='select'),
		url(r'^save-image/$', views.save_image, name='save-image'),
		)