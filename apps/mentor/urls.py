from django.conf.urls import patterns, url
from apps.mentor import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^register/$', views.register, name='index'))
