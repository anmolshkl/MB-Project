from django.conf.urls import patterns, url
from apps.mentor import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^register/$', views.register, name='index'),
                       url(r'^self-profile/$', views.self_profile_view, name="self_profile_view"),
                       url(r'^edit-profile/$', views.edit_profile, name="edit_profile"),
                       url(r'^get-profile/(?P<mentorid>\w+)/$', views.get_profile, name="get_profile_data"),
                       url(r'^get-data/$', views.get_data, name="get_data"),
                       url(r'^send-request/$', views.send_request, name="send call request"),
                       url(r'^live/$', views.live, name="get_data"),
                       url(r'^manage-social-profiles/(?P<action>\w+)/(?P<provider>\w+)/$', views.manage_social_profiles,
                           name="remove-social-profiles"),
                       url(r'^manage-social-profiles/$', views.manage_social_profiles, name="manage-social-profiles"),
                       url(r'^checkAvailability/$', views.check_availability, name="check-availability"),
                       )