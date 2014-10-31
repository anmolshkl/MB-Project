from django.conf.urls import patterns, url
from apps.mentor import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^register/$', views.register, name='index'),
        url(r'^self-profile/$',views.self_profile_view,name="self_profile_view"),
		url(r'^edit-profile/$',views.edit_profile,name="edit_profile"),
		url(r'^get-data/$',views.get_data,name="get_data"))