from django.conf.urls import patterns, url
from apps.mentee import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^register/$', views.register, name='index'),
        url(r'^self-profile/$',views.self_profile_view,name="self_profile_view"))